"""
TODO: need to describe a save-file map
"""

import os
import re

import datasheets

class SaveSlot:
    """

    """

    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.macros: list = []
        self.weapon_list: list = []
        self.armor_head_list: list = []
        self.armor_torso_list: list = []
        self.armor_hands_list: list = []
        self.armor_legs_list: list = []
        self.talisman_list: list = []
        self.spell_list: list = []
        # self.item_list: list = []


def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.

    :return: Path as string
    """
    return os.getcwd() + r'\test\ER0000_controls_test.sl2'
    # return os.getcwd() + r'\test\ER0000_Talismans.sl2'
    # return os.getcwd() + r'\test\ER0000_125_windhalberds_mooninhands_claymore_chest.sl2'
    # return os.getcwd() + r'\test\ER0000_freedom_something_in_inventory.sl2'


def range_before_save_slots() -> int:
    """
    Returns an amount of symbols in HEX-save-file that goes before
    first save-slot information starts.
    """
    return 0x0000310


def slot_ranges(save_slot_number: int = 0) -> tuple | list:
    """
    Returns hex interval for the save slot in save file.
    If save_slot_number is 0, returns a list of all 10 intervals.
    """

    between_slots = 16
    save_slot_width = 2621456

    intervals = [(range_before_save_slots(), 0x0280310)]  # First save file.
    for _ in range(9):
        last_interval = intervals[-1]
        new_interval_begin = last_interval[1] + between_slots
        new_interval_end = last_interval[1] + save_slot_width
        intervals.append((new_interval_begin, new_interval_end))

    if save_slot_number == 0:
        return intervals
    else:
        return intervals[save_slot_number - 1]


def slot_names_ranges() -> tuple:
    """
    Returns HEX-ranges of places in save-file that keeps save slot names
    (characters names).
    """

    return ((0x1901d0e, 0x1901d0e + 32),
            (0x1901f5a, 0x1901f5a + 32),
            (0x19021a6, 0x19021a6 + 32),
            (0x19023f2, 0x19023f2 + 32),
            (0x190263e, 0x190263e + 32),
            (0x190288a, 0x190288a + 32),
            (0x1902ad6, 0x1902ad6 + 32),
            (0x1902d22, 0x1902d22 + 32),
            (0x1902f6e, 0x1902f6e + 32),
            (0x19031ba, 0x19031ba + 32))


def control_keys_ranges() -> dict:
    """
    Returns HEX-ranges of places in save-file that keeps controls for some
    actions that could be used in macros.
    """

    return {
        'roll': 0x01903541,
        'jump': 0x01903555,
        'crouch': 0x0190352d,
        'reset_camera': 0x019035b9,
        'switch_spell': 0x019035cd,
        'switch_item': 0x019035e1,
        'attack': 0x0190361d,
        'strong_attack': 0x019035cd,
        'guard': 0x01903645,
        'skill': 0x01903659,
        'use_item': 0x0190366d,
        'event_action': 0x01903681,
    }


def control_keys_values() -> dict:
    """
    Returns values for keys that are used in save-file to define what key is
    used for a control. Values are in decimal.
    For example, "Num4" ("144" dec.) would be "90" in HEX-file.
    """

    return {
        128: 'F1',
        129: 'F2',
        130: 'F3',
        131: 'F4',
        132: 'F5',
        133: 'F6',
        134: 'F7',
        135: 'F8',
        136: 'F9',
        137: 'F10',
        156: 'F11',
        157: 'F12',
        80: '0',
        71: '1',
        72: '2',
        73: '3',
        74: '4',
        75: '5',
        76: '6',
        77: '7',
        78: '8',
        79: '9',
        151: 'Num0',
        148: 'Num1',
        149: 'Num2',
        150: 'Num3',
        144: 'Num4',
        145: 'Num5',
        146: 'Num6',
        140: 'Num7',
        141: 'Num8',
        142: 'Num9',
        99: 'A',
        117: 'B',
        115: 'C',
        101: 'D',
        87: 'E',
        102: 'F',
        103: 'G',
        104: 'H',
        92: 'I',
        105: 'J',
        106: 'K',
        107: 'L',
        119: 'M',
        118: 'N',
        93: 'O',
        94: 'P',
        85: 'Q',
        88: 'R',
        100: 'S',
        89: 'T',
        91: 'U',
        116: 'V',
        86: 'W',
        114: 'X',
        90: 'Y',
        113: 'Z',
        84: 'Tab',
        111: 'Shift (left)',
        123: 'Shift (right)',
        98: 'Control (left)',
        226: 'Control (right)',
        83: 'Backspace',
        126: 'Space',
        97: 'Enter (main)',
        225: 'Enter (numpad)',
        125: 'Alt (left)',
        268: 'Home',
        188: 'PageUp',
        194: 'End',
        196: 'PageDown',
        197: 'Insert',
        198: 'Delete'
    }


def instances_search_range(slot_data: bytes,
                           slot_name: str) -> tuple:
    """
    Seeks for a range in which can be found instances of equipment in specific
    save slot data. Minimal range is a position of slot data name.
    Max range can't be calculated and is taken with a margin.
    """

    slot_name_hex = bytes(slot_name, 'utf-8')
    slot_name_hex_bytes = [bytes.fromhex(hex(x)[2:]) for x in slot_name_hex]
    slot_name_hex_bytes = [x + bytes.fromhex('00') for x in
                           slot_name_hex_bytes]
    slot_name_hex = b''.join(slot_name_hex_bytes)

    slot_name_position = slot_data.find(slot_name_hex)

    range_max = 0x00035000

    return slot_name_position, range_max


def inventory_and_chest_separator() -> bytes:
    """
    Returns a HEX-string that separates inventory and chest block for
    weapon searching.
    """
    return bytes.fromhex('ffffffff00000000') * 6


def get_slot_data(filepath: str, save_slot_number: int = 0) -> bytes:
    """
    Returns hex data of save file related to specific save slot.
    Returns full data of save file is safe slot is not specified.
    :param filepath: path to savefile
    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """
    with open(filepath, "rb") as fh:
        data = fh.read()

        if not save_slot_number:
            return data

        slot_interval = slot_ranges(save_slot_number)

        return data[slot_interval[0]:slot_interval[1]]


def get_slot_names(file) -> list:
    """

    :param file:
    :return:
    """
    # try:
    with open(file, "rb") as fh:
        data = fh.read()

    # except FileNotFoundError as e:
    #     return False

    names_ranges = slot_names_ranges()
    names = [data[begin:end].decode('utf-16') for begin, end in names_ranges]
    names = list(map(lambda x: x.strip('\x00'), names))

    return names


def endian_turn(hex_string: str) -> str:
    """
    Turns little-endian hex string to big-endian or visa versa,
    Example: 8097FA01 <-> 01FA9780
    :param hex_string: hex string
    :return: None
    """

    if len(hex_string) < 2:
        return hex_string

    if len(hex_string) % 2 == 1:
        return hex_string

    pairs = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]

    return ''.join(reversed(pairs))


def item_id_as_hex(item_id: str, max_length: int) -> str:
    """

    """

    hex_big_endian = hex(int(item_id))[2:]
    if len(hex_big_endian) % 2 == 1:
        hex_big_endian = '0' + hex_big_endian
    hex_little_endian = endian_turn(hex_big_endian)
    hex_little_endian += (max_length - len(hex_little_endian)) * '0'

    return hex_little_endian


def add_escaping_character_to_byte_reg(reg_expression: bytes) -> bytes:
    """

    :param reg_expression:
    :return:
    """

    escaping_characters = [b'\\', b'[', b']', b'(', b')', b'|',
                           b'^', b'$', b'.', b'?', b'*', b'+']
    for ch in escaping_characters:
        reg_expression = reg_expression.replace(ch, b'\\' + ch)

    return reg_expression


def get_all_equipment(save_file_path: str, slot_number: int):
    """
    code keeper
    :return:
    """

    slot_data = get_slot_data(save_file_path, slot_number)
    slot_name = get_slot_names(save_file_path)[slot_number - 1]

    # Looking for all equipment mentioned in save-file, whatever quantity
    # and position in inventory or chest.
    slot_data_for_equipment_search = slot_data[:0x00030000]
    all_equipment_having = []
    for weapon in datasheets.weapons():
        weapon_id = weapon[1]
        weapon_name = weapon[2]
        if bytes.fromhex(weapon_id) in slot_data_for_equipment_search:
            all_equipment_having.append([weapon_name, weapon_id, 'Weapons'])

    for armor in datasheets.armor():
        armor_id = armor[1]
        armor_name = armor[2]
        if bytes.fromhex(armor_id) in slot_data_for_equipment_search:
            all_equipment_having.append([armor_name, armor_id, 'Armor'])

    # Looking for many instances of each equipment. In save-file structure
    # is like this: [inventory instances]-[separator]-[chest instances]
    # We need only inventory instances, so first we need to find the separator.

    instances_range = instances_search_range(slot_data, slot_name)
    data_for_instances_search = slot_data[instances_range[0]:
                                          instances_range[1]]
    separator = inventory_and_chest_separator()
    separator_pos = data_for_instances_search.find(separator)

    inventory_list = []
    for equipment in all_equipment_having:
        equipment_name = equipment[0]
        equipment_id = equipment[1]
        equipment_type = equipment[2]
        equipment_mark = '8080'
        if equipment_type == 'Armor':
            equipment_mark = '8090'

        # In save-file we're looking for lines like: ID ID 80 MM WW WW WW (WW)
        # Where:
        #   ID ID - ID of specific instance of equipment.
        #   80 MM - mark of equipment. "80 80" for weapon, "80 90" for armor.
        #   WW WW WW (WW) - equipment ID. Weapon has 4 pieces, armor has 3.
        # Each line represents an instance of equipment.
        id_for_reg = bytes.fromhex(equipment_mark + equipment_id)
        id_for_reg = add_escaping_character_to_byte_reg(id_for_reg)
        reg_expression = b'.{2}(?=' + id_for_reg + b')'

        result = re.finditer(reg_expression,
                             slot_data[:instances_range[0] + separator_pos])

        for match in result:

            instance_id = match.group() + bytes.fromhex(equipment_mark)
            instance_position = data_for_instances_search.find(instance_id)
            if instance_position < 0:
                continue

            # As we found instance's ID, we can see, in what part this ID
            # is located. If it's in inventory part, then that's it.
            if instance_position > separator_pos:
                continue

            instance_id = instance_id.hex(' ').replace(' ', '')
            position_in_file = hex(instances_range[0]
                                   + instance_position
                                   + range_before_save_slots())

            # We have to learn in what order equipment is placed in inventory
            # if inventory is sorted as "Ascending Order of Acquisition".
            # Instance's ID is located in line that looks like:
            # ID ID 80 80 XX XX XX XX NN NN
            # Where:
            #   ID ID - instance's ID
            #   80 80 XX XX XX XX - not interesting data
            #   NN NN - additional ID that can be used to learn what order in
            #           inventory this instance has if inventory is sorted as
            #           "Ascending Order of Acquisition".
            inventory_order_id = data_for_instances_search[
                                 instance_position + 8:
                                 instance_position + 10]
            inventory_order_id = inventory_order_id.hex(' ').replace(' ', '')

            # Order ID has two HEX numbers ("f1 21") but actual order goes
            # on mirrored numbers ("21 f1", "21 f2", "21 f3" etc.)
            inventory_order_id = inventory_order_id[2:4] + \
                                 inventory_order_id[:2]

            # We need to check what type of armor an instance has.
            if equipment_type == 'Armor':
                equipment_id_decimal = str(int(endian_turn(equipment_id), 16))
                if equipment_id_decimal.endswith('000'):
                    equipment_type += '_Head'
                elif equipment_id_decimal.endswith('100'):
                    equipment_type += '_Torso'
                elif equipment_id_decimal.endswith('200'):
                    equipment_type += '_Hands'
                elif equipment_id_decimal.endswith('300'):
                    equipment_type += '_Legs'

            instance_dict = {}
            instance_dict.setdefault('equipment_type', equipment_type)
            instance_dict.setdefault('equipment_name', equipment_name)
            instance_dict.setdefault('equipment_id', equipment_id)
            instance_dict.setdefault('instance_id', instance_id)
            instance_dict.setdefault('inventory_order_id', inventory_order_id)
            instance_dict.setdefault('position', position_in_file)
            inventory_list.append(instance_dict)

    # Ta lismans are located in save-file simmilar to armor and weapons, but
    # not identical.
    # Talisman line looks like: XX XX 00A001000000 NN NN, where
    #   XX XX - talisman ID.
    #   00A001000000 - always identical part
    #   NN NN - order ID.
    #
    # Inventory/Chest search is identical to weapons and armor.
    # Talismans don't have instances, you can only have one.
    talisman_mark = '00A001000000'
    for talisman in datasheets.talismans():
        talisman_id = talisman[1]
        talisman_name = talisman[2]

        talisman_search = bytes.fromhex(talisman_id + talisman_mark)
        talisman_position = data_for_instances_search.find(talisman_search)
        if talisman_position < 0:
            continue

        if talisman_position > separator_pos:
            continue

        position_in_file = hex(instances_range[0]
                               + talisman_position
                               + range_before_save_slots())

        inventory_order_id = data_for_instances_search[
                             talisman_position + 8:
                             talisman_position + 10]
        inventory_order_id = inventory_order_id.hex(' ').replace(' ', '')
        inventory_order_id = inventory_order_id[2:4] + inventory_order_id[:2]

        instance_dict = {}
        instance_dict.setdefault('equipment_type', 'Talismans')
        instance_dict.setdefault('equipment_name', talisman_name)
        instance_dict.setdefault('equipment_id', talisman_id)
        instance_dict.setdefault('instance_id', '')
        instance_dict.setdefault('inventory_order_id', inventory_order_id)
        instance_dict.setdefault('position', position_in_file)
        inventory_list.append(instance_dict)

    # Chosen spells can be found pretty easily.
    # Spell line looks like SS SS 00 00 FF FF
    # Where:
    #   SS SS - spell ID
    #   00 00 FF FF - mark of chosen spell
    # In save-file these lines are in order identical to order in game.
    for spell in datasheets.spells():
        spell_id = spell[1]
        spell_name = spell[2]
        spell_mark = '0000FFFF'
        spell_search = bytes.fromhex(spell_id + spell_mark)

        spell_position = data_for_instances_search.find(spell_search)
        if spell_position < 0:
            continue

        position_in_file = hex(instances_range[0]
                               + spell_position
                               + range_before_save_slots())

        inventory_order_id = position_in_file[2:]

        instance_dict = {}
        instance_dict.setdefault('equipment_type', 'Spells')
        instance_dict.setdefault('equipment_name', spell_name)
        instance_dict.setdefault('equipment_id', spell_id)
        instance_dict.setdefault('instance_id', '')
        instance_dict.setdefault('inventory_order_id', inventory_order_id)
        instance_dict.setdefault('position', position_in_file)
        inventory_list.append(instance_dict)

    sorted_equipment = sorted(inventory_list,
                              key=lambda x: (x['equipment_type'],
                                             int(x['inventory_order_id'], 16)))
    result = {
        'Weapons': [],
        'Talismans': [],
        'Armor_Head': [],
        'Armor_Torso': [],
        'Armor_Hands': [],
        'Armor_Legs': [],
        'Spells': [],
    }

    for equipment in sorted_equipment:
        result[equipment['equipment_type']].append(equipment)

    return result
