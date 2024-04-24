from __future__ import annotations
import os
import sys
import asyncio
import shutil
import logging
from typing import Dict, Any, Set

import ModuleUpdate
ModuleUpdate.update()
import Utils
from .Items import item_dictionary_table, item_counts

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

    local_psy_location_to_local_psy_item_id: Dict[int, int]
    local_psy_item_ids: Set[int]

    def __init__(self, server_address, password):
        super(PsychonautsContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.got_deathlink = False
        self.deathlink_status = False
        self.psy_item_counts = {item_dictionary_table[item_name]: count for item_name, count in item_counts.items()}
        self.psy_item_counts_received = {k: 0 for k in self.psy_item_counts.keys()}
        self.slot_data = {}
        self.local_psy_location_to_local_psy_item_id = {}
        self.local_psy_item_ids = set()

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

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.slot_data = args.get("slot_data", {})
            # When int keys are stored in slot data, they are converted to str, so convert back to int.
            self.local_psy_location_to_local_psy_item_id = {int(k): v for k, v in self.slot_data["local_location_to_psy_id"].items()}
            self.local_psy_item_ids = set(self.local_psy_location_to_local_psy_item_id.values())
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
                for item in args['items']:
                    # subtract base_id to get real value for game
                    network_item = NetworkItem(*item)
                    converted_id = network_item.item - 42690000

                    # Total number of these items available to the game.
                    item_count = self.psy_item_counts[converted_id]
                    # Maximum Psychonauts ID for this item when there are multiple copies.
                    max_converted_id = converted_id + item_count - 1

                    # Check if the item was placed locally.
                    if network_item.player == self.slot:
                        # Locally placed items must write the exact Psychonauts item ID they were placed as.
                        converted_location_id = network_item.location - 42690000
                        if converted_location_id not in self.local_psy_location_to_local_psy_item_id:
                            print(f"Error: Could not find {converted_location_id} in"
                                  f" {self.local_psy_location_to_local_psy_item_id}")
                        else:
                            # Get the Psychonauts item id for the item at this location
                            local_item_psy_id = self.local_psy_location_to_local_psy_item_id[converted_location_id]
                            # Check that the Psychonauts ID matches the item AP thinks is at this location.
                            if converted_id <= local_item_psy_id <= max_converted_id:
                                with open(os.path.join(self.game_communication_path, "ItemsReceived.txt"), 'a') as f:
                                    f.write(f"{local_item_psy_id}\n")
                            else:
                                # This should not happen unless the slot data does not match the multiworld data.
                                print(f"Error: The local item AP thinks is at {converted_location_id} has base ID"
                                      f" '{converted_id}' and max ID '{max_converted_id}', but the actual local item"
                                      f" according to slot data has ID '{local_item_psy_id}'")

                    else:
                        # Total number of these items received by the game so far
                        item_count_received = self.psy_item_counts_received[converted_id]
                        # For non-local received items, the Psychonauts ID is incremented for each copy of that received
                        # so far, so that each item received produces a unique Psychonauts ID.
                        next_psy_id = converted_id + item_count_received
                        # Psychonauts has a limited number of IDs for each duplicate of an item, so check if it's
                        # possible to send more of this item.
                        if next_psy_id in self.local_psy_item_ids or next_psy_id > max_converted_id:
                            # Locally placed Psychonauts items are placed starting from that item's maximum ID and
                            # decrementing the ID for each item placed, so reaching the Psychonauts ID of a locally
                            # placed item means that all copies of this item have been received or placed locally.
                            # When forcefully sending an item via server console cheat command, items are sent and
                            # collected from locations that exist first, so reaching the ID of a locally placed item
                            # should only occur when all locations, including local locations, containing this item
                            # have been exhausted.
                            #
                            # Alternatively, if there were no locally placed copies of the item, then Psychonauts will
                            # only have run out of IDs for the item once the maximum ID for that item has been reached.
                            print(f"Warning: Cannot send item '{network_item.item}' with Psychonauts ID '{next_psy_id}'"
                                  f" and base Psychonauts ID '{converted_id}' because Psychonauts has run out of that"
                                  f"item.")
                        else:
                            with open(os.path.join(self.game_communication_path, "ItemsReceived.txt"), 'a') as f:
                                f.write(f"{next_psy_id}\n")
                            # Increment the received count for this item.
                            self.psy_item_counts_received[converted_id] = item_count_received + 1


        if cmd in {"RoomUpdate"}:

            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

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
                    sending = sending+[(int(value + 42690000))]
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



