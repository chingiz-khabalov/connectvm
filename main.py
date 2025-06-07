#!/bin/python3
import sys
import pexpect
import os.path
from typing import Dict, List, Optional


CONFIG_FOLDER = "~/.config/connectvm"
CONFIG_FOLDER = os.path.expanduser(CONFIG_FOLDER)

ADDRESSES_PATH = os.path.join(CONFIG_FOLDER, "addresses")


def attach(name: str, user: Optional[str] = None, port: Optional[int] = None):
    address = get_addresses()[name]
    if user is None:
        user = address[0]
    if port is None:
        port = address[2]
    ssh_command = f"ssh -p {port} {user}@{address[1]}"
    connection = pexpect.spawn(ssh_command)
    connection.interact()


def get_addresses() -> Dict[str, List[str]]:
    addresses = dict()
    if not os.path.exists(ADDRESSES_PATH):
        return addresses

    with open(ADDRESSES_PATH, "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            name, address = line.split("=")
            address = address.split(";")
            addresses[name] = address

    return addresses


def write_addresses(addresses: Dict[str, List[str]]):
    with open(ADDRESSES_PATH, "w") as file:
        lines = list()
        for name, address in addresses.items():
            lines.append(f"{name}={';'.join([str(addr) for addr in address])}\n")

        file.writelines(lines)


def is_decimal(line: str):
    return all(i.isdigit() for i in line)


def clone_name(name: str, new_name: str):
    cloning_address = get_addresses()[name]
    address = dict()
    for index, field_name in enumerate(["user", "address", "port"]):
        address[field_name] = cloning_address[index]

    result = ask_address(address)
    save(new_name, *result)


def save(name, user, address, port=22):
    addresses = get_addresses()
    addresses[name] = [user, address, port]
    write_addresses(addresses)


def ask_address(defaults: dict = None) -> list:
    if defaults is None:
        defaults = dict()

    query = f"User:"
    username = defaults.get("user")
    if username is not None:
        query += f" leave blank for {username}"
    user = input(query + "\n")
    user = user if user else defaults["user"]

    query = f"Address:"
    address = defaults.get("address")
    if address is not None:
        query += f" leave blank for {address}"
    address = input(query + "\n")
    address = address if address else defaults["address"]

    success = False
    port = str()
    while not success:
        port = input(f"Port (blank for {defaults.setdefault('port', '22')}):\n")
        if not is_decimal(port):
            print("Invalid non numeric port, try again")
        else:
            success = True

    if port == "":
        port = defaults["port"]
    else:
        port = int(port)

    return [user, address, port]


def set_name(name: str):
    full_address = ask_address()
    save(name, *full_address)


def edit_name(name: str):
    addresses = get_addresses()

    for num, field_name in enumerate(["User", "Address", "Port"]):
        result = input(f"{field_name} (leave blank to not edit):\n")
        if result.strip() != "":
            addresses[name][num] = result

    write_addresses(addresses)


def main():
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER, exist_ok=True)

    arguments = sys.argv

    if len(arguments) < 2:
        print("Not enough arguments")
        return

    command = arguments[1]
    if command == "list":
        for key, value in get_addresses().items():
            print(f"{key} = {value[0]}@{value[1]}:{value[2]}")
        return

    elif command == "completion_list":
        print(" ".join(["clone", "names", "list", "set", "delete", "attach", "edit"]))
        return

    elif command == "names":
        print(" ".join(list(get_addresses().keys())))
        return

    if len(arguments) < 3:
        print("hostname for command not specified")
        return
    
    name = arguments[2]

    if command == "set":
        set_name(name)
        return

    addresses = get_addresses()
    if name not in addresses.keys():
        print(f"Invalid name: {name}")
        return
    
    if command == "clone":
        if len(arguments) < 4:
            print("specify the new name")
            return
        new_name = arguments[3]
        clone_name(name, new_name)
        return

    elif command == "delete":
        addresses.pop(name)
        write_addresses(addresses)
        return

    elif command == "edit":
        edit_name(name)
        return

    elif command == "attach":
        if len(arguments) == 3:
            attach(name)
            return

        else:
            port = arguments[3]
            if not is_decimal(port):
                print(f"Invalid port \"{port}\"")
                return

            port = int(arguments[2])
            attach(arguments[1], port=port)
            return

    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()
