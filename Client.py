from __future__ import annotations
import os
import queue
import sys
import asyncio
import shutil
import logging
from typing import Dict, Any, Set, List
from queue import SimpleQueue
from threading import Lock

import ModuleUpdate
ModuleUpdate.update()
import Utils
from .Items import item_dictionary_table, item_counts, AP_ITEM_OFFSET
from .Locations import AP_LOCATION_OFFSET, all_fillable_locations

logger = logging.getLogger("Client")

if __name__ == "__main__":
    Utils.init_logging("PsychonautsClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

# using this to find the folder game was launched from
# then find ModData folder there
def find_moddata_folder(root_directory):
    moddata_folder = os.path.join(root_directory, "ModData")
    if os.path.exists(moddata_folder):
        return moddata_folder
    else:
        print_error_and_close("PsychonautsClient couldn't find ModData folder. "
                                  "Unable to infer required game_communication_path")


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

class PsychonautsClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
    
    def _cmd_deathlink(self):
        """Toggles Deathlink"""
        if isinstance(self.ctx, PsychonautsContext):
            self.ctx.deathlink_status = not self.ctx.deathlink_status
            if self.ctx.deathlink_status:
                self.output(f"Deathlink enabled.")
            else:
                self.output(f"Deathlink disabled.")

class PsychonautsContext(CommonContext):
    command_processor: int = PsychonautsClientCommandProcessor
    game = "Psychonauts"
    items_handling = 0b111  # full remote

    max_item_counts: Dict[int, int]
    non_local_received_item_counts: Dict[int, int]
    local_psy_location_to_local_psy_item_id: Dict[int, int]
    local_psy_item_ids: Set[int]
    slot_data: Dict[str, Any]
    has_local_location_data: bool
    pending_received_items: List[NetworkItem]
    pending_received_items_lock: Lock

    def __init__(self, server_address, password):
        super(PsychonautsContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.got_deathlink = False
        self.deathlink_status = False

        # The maximum number of each item that Psychonauts can receive before it runs out of unique IDs for that item.
        self.max_item_counts = {item_dictionary_table[item_name] + AP_ITEM_OFFSET: count
                                for item_name, count in item_counts.items()}
        # The number of times each item has been received from a non-local location.
        self.non_local_received_item_counts = {item_id: 0 for item_id in self.max_item_counts.keys()}

        self.slot_data = {}

        # Pre-scout all local locations so that the client can figure out the Psychonauts item IDs of all locally placed
        # items.
        self.locations_scouted.update((location_id + AP_LOCATION_OFFSET for location_id in all_fillable_locations.values()))

        # These are read from slot data:
        # Mapping from Psychonauts location ID to Psychonauts item ID for all locally placed items.
        self.local_psy_location_to_local_psy_item_id = {}
        # Set of Psychonauts item IDs of locally placed items. These IDs cannot be used when receiving non-local items.
        self.local_psy_item_ids = set()

        self.has_local_location_data = False
        self.pending_received_items = []
        self.pending_received_items_lock = Lock()

        options = Utils.get_settings()
        root_directory = options["psychonauts_options"]["root_directory"]
        
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        moddata_folder = find_moddata_folder(root_directory)
        self.game_communication_path = moddata_folder


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(PsychonautsContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(PsychonautsContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if "Items" not in file and "Deathlink" not in file:
                    os.remove(root+"/"+file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(PsychonautsContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if "Items" not in file and "Deathlink" not in file:
                    os.remove(root+"/"+file)

    def set_up_local_psy_item_id_info(self):
        if not self.has_local_location_data:
            # attempt to set it up
            scouted_location_info = {}
            for psy_location_id in all_fillable_locations.values():
                ap_location_id = psy_location_id + AP_LOCATION_OFFSET
                scouted_network_item = self.locations_info.get(ap_location_id)
                if scouted_network_item is None:
                    print("Have not received scouted local location info")
                    return False
                scouted_location_info[psy_location_id] = scouted_network_item

            # All the information needed to figure out the Psychonaunts item IDs of locally placed items has been
            # acquired.

            current_local_ids = {}
            for item_name, psy_item_id in item_dictionary_table.items():
                max_psy_item_id = psy_item_id + item_counts[item_name] - 1
                current_local_ids[psy_item_id] = max_psy_item_id

            local_psy_location_to_local_psy_item_id = {}
            for psy_location_id in sorted(all_fillable_locations.values()):
                scouted_network_item = scouted_location_info[psy_location_id]
                psy_item_id = scouted_network_item.item - AP_ITEM_OFFSET
                current_psy_id = current_local_ids.get(psy_item_id)
                if current_psy_id is None:
                    # The item is non-local, so can be ignored.
                    continue
                local_psy_location_to_local_psy_item_id[psy_location_id] = current_psy_id
                # Locally placed items start at their maximum Psychonauts ID, decrementing each time a copy of that item
                # is placed. This ensures that each copy has a unique Psychonauts ID.
                current_local_ids[psy_item_id] = current_psy_id - 1
            self.local_psy_location_to_local_psy_item_id = local_psy_location_to_local_psy_item_id
            self.local_psy_item_ids = set(local_psy_location_to_local_psy_item_id.values())
            self.has_local_location_data = True
            print("Scouted location location info has been received and processed")

        return True

    def receive_item(self, network_item: NetworkItem):
        if not self.has_local_location_data:
            raise RuntimeError("receive_item was called before local location data has been received and set")
        ap_item_id = network_item.item
        # Subtract the AP item offset to get the base item ID for Psychonauts.
        base_psy_item_id = ap_item_id - AP_ITEM_OFFSET

        # The maximum number of times this item can be received by Psychonauts.
        max_item_count = self.max_item_counts[ap_item_id]
        # Maximum Psychonauts ID for this item when there are multiple copies.
        max_psy_item_id = base_psy_item_id + max_item_count - 1

        # Check if the item was placed locally.
        if network_item.player == self.slot:
            # Locally placed items must write the exact Psychonauts item ID they were placed as.
            # Writing locally placed items is required for sending local items via server cheat commands as
            # well as resuming an in-progress slot from a new save file without having to manually collect
            # the local items again.
            psy_location_id = network_item.location - AP_LOCATION_OFFSET
            if psy_location_id not in self.local_psy_location_to_local_psy_item_id:
                # This should not happen unless AP can send dummy local location IDs for locations that do
                # not exist.
                print(f"Error: Could not find location '{network_item.location}' (converted to"
                      f" '{psy_location_id}') in the known local location IDs:"
                      f" {self.local_psy_location_to_local_psy_item_id.keys()}")
            else:
                # Get the Psychonauts item id for the item at this local location.
                local_item_psy_id = self.local_psy_location_to_local_psy_item_id[psy_location_id]
                # Check that the Psychonauts ID matches the item AP thinks is at this location.
                if base_psy_item_id <= local_item_psy_id <= max_psy_item_id:
                    with open(os.path.join(self.game_communication_path, "ItemsReceived.txt"), 'a') as f:
                        f.write(f"{local_item_psy_id}\n")
                else:
                    # This should not happen unless the slot data does not match the multiworld data.
                    print(f"Error: The local item that AP thinks is at '{psy_location_id}' has Psychonauts"
                          f" base ID '{base_psy_item_id}' and max ID '{max_psy_item_id}', but the actual"
                          f" local item according to slot data has Psychonauts ID '{local_item_psy_id}'")

        else:
            # For non-local received items, the Psychonauts ID is incremented for each copy of that received
            # so far, so that each item received produces a unique Psychonauts ID.
            # Count of this item received from other worlds so far.
            item_count_received = self.non_local_received_item_counts[ap_item_id]
            psy_item_id = base_psy_item_id + item_count_received
            # Psychonauts has a limited number of IDs for each duplicate of an item, so check if it's
            # possible to send more of this item.
            if psy_item_id in self.local_psy_item_ids or psy_item_id > max_psy_item_id:
                # Locally placed Psychonauts items are placed starting from that item's maximum ID and
                # decrementing the ID for each item placed, so reaching the Psychonauts ID of a locally
                # placed item means that all available copies of this item have been received or placed
                # locally.
                # When forcefully sending an item via server console cheat command, items are sent and
                # collected from locations that exist first, so reaching the ID of a locally placed item
                # should only occur when all locations, including local locations, have been exhausted.
                #
                # Alternatively, if there were no locally placed copies of the item, then Psychonauts will
                # only have run out of IDs for the item once the maximum ID for that item has been reached.
                print(f"Warning: Cannot receive AP item '{ap_item_id}' with incremented Psychonauts ID"
                      f" '{psy_item_id}' and base Psychonauts ID '{base_psy_item_id}' because Psychonauts"
                      f" has run out of unique IDs for that item. The maximum Psychonauts ID for this item,"
                      f" including locally placed items, is '{max_psy_item_id}'.")
            else:
                with open(os.path.join(self.game_communication_path, "ItemsReceived.txt"), 'a') as f:
                    f.write(f"{psy_item_id}\n")
                # Increment the received count for this item.
                self.non_local_received_item_counts[ap_item_id] = item_count_received + 1

    def on_package(self, cmd: str, args: dict):
        print(f"Received: '{cmd}'")
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            # create ItemsCollected.txt if it doesn't exist yet
                
            # Path to the ItemsCollected.txt file inside the ModData folder
            items_collected_path = os.path.join(self.game_communication_path, "ItemsCollected.txt")
            if not os.path.exists(items_collected_path):
                with open(items_collected_path, 'w') as f:
                    f.write(f"")
                    f.close()
            # empty ItemsReceived.txt to avoid appending duplicate items lists
            with open(os.path.join(self.game_communication_path, "ItemsReceived.txt"), 'w') as f:
                f.write(f"")
                f.close()
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                if self.set_up_local_psy_item_id_info():
                    for item in args['items']:
                        network_item = NetworkItem(*item)
                        self.receive_item(network_item)
                else:
                    print("Have not received scouted location info, so storing items to receive until later")
                    try:
                        #self.pending_received_items_lock.acquire()
                        for item in args['items']:
                            network_item = NetworkItem(*item)
                            self.pending_received_items.append(network_item)
                    finally:
                        #self.pending_received_items_lock.release()
                        pass

        if cmd in {"RoomUpdate"}:

            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

        if cmd == "LocationInfo":
            if not self.has_local_location_data:
                # It could be the response to the initial LocationScouts request that was sent out.
                # Try to set up the local item data and receive any pending received items
                if self.set_up_local_psy_item_id_info():
                    print("We have received the scouted location info we were waiting for and have set up the local data")
                    if self.pending_received_items:
                        print("There were pending received items to process, so processing them now")
                        try:
                            #self.pending_received_items_lock.acquire()
                            for network_item in self.pending_received_items:
                                self.receive_item(network_item)
                            self.pending_received_items.clear()
                        finally:
                            #self.pending_received_items_lock.release()
                            pass

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class PsychonautsManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Psychonauts Client"

        self.ui = PsychonautsManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_deathlink(self, data: Dict[str, Any]):
        self.got_deathlink = True
        super().on_deathlink(data)

async def game_watcher(ctx: PsychonautsContext):
    from worlds.psychonauts.Locations import all_locations
    while not ctx.exit_event.is_set():
        # Check for DeathLink toggle
        await ctx.update_death_link(ctx.deathlink_status)

        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        
        # Check for Deathlink to send to player
        if ctx.got_deathlink:
            ctx.got_deathlink = False
            with open(os.path.join(ctx.game_communication_path, "DeathlinkIn.txt"), 'a') as f:
                f.write("DEATH\n")
                f.close()
        
        # Check for Deathlinks from player
        with open(os.path.join(ctx.game_communication_path, "DeathlinkOut.txt"), 'r+') as f:
            RazDied = f.read()
            if RazDied:
                # Move the file pointer to the beginning
                f.seek(0)
                # Empty the file by writing an empty string
                f.truncate(0)
                if "DeathLink" in ctx.tags:
                    await ctx.send_death(death_text = f"{ctx.player_names[ctx.slot]} became lost in thought!")
            f.close
        
        sending = []
        # Initialize an empty table
        collected_table = []
        victory = False
        
        # Open the file in read mode
        with open(os.path.join(ctx.game_communication_path, "ItemsCollected.txt"), 'r') as f:
            collected_items = f.readlines()            
            # Iterate over each line in the file
            for line in collected_items:
                # Convert the line to a float and add it to the table
                value = float(line.strip())
                # Keep track of already collected values
                if value not in collected_table:
                    # add the base_id 42690000
                    sending = sending+[(int(value + AP_LOCATION_OFFSET))]
                    collected_table.append(value)
            f.close()

        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("victory.txt") > -1:
                    victory = True
                    
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory == True:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch():
    async def main(args):
        ctx = PsychonautsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="PsychonautsProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Psychonauts Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()



