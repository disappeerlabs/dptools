"""
helpers.py	

helper object and functions for setting up gpg test keys

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import tempfile
import gnupg

alice_key_vals_dict = {"Name": "alice",
                       "Email": "alice@email.com",
                       "Comment": "alice comment message",
                       "Key Length": "2048",
                       "Key Type": "RSA",
                       "Key Usage": "",
                       "Subkey Type": "ELG-E",
                       "Subkey Length": "2048",
                       "Expire Date": "2030-04-01",
                       "Passphrase": "passphrase"
                       }
bob_key_vals_dict = {"Name": "bob",
                     "Email": "bob@email.com",
                     "Comment": "bob comment message",
                     "Key Length": "2048",
                     "Key Type": "RSA",
                     "Key Usage": "",
                     "Subkey Type": "ELG-E",
                     "Subkey Length": "2048",
                     "Expire Date": "2030-04-01",
                     "Passphrase": "passphrase"
                     }
key_reference_dict = {"Name": "name_real",
                      "Email": "name_email",
                      "Comment": "name_comment",
                      "Key Length": "key_length",
                      "Key Type": "key_type",
                      "Key Usage": "key_usage",
                      "Subkey Type": "subkey_type",
                      "Subkey Length": "subkey_length",
                      "Expire Date": "expire_date",
                      "Passphrase": "passphrase"
                      }


def create_key_input_dict(key_ref_dict, key_input_val_dict):
    """Take key vals dict as input, return dict structured for key creation"""
    new_key_default_vals_dict = key_input_val_dict
    new_key_input_dict = key_ref_dict
    final_key_dict = {}
    for item in new_key_input_dict:
        key = new_key_input_dict[item]
        val = new_key_default_vals_dict[item]
        final_key_dict[key] = val
    return final_key_dict


class SetUpKeys:

    passphrase = 'passphrase'

    def __init__(self):
        self.temp_dir_alice = tempfile.TemporaryDirectory()
        self.alice_dir_path = self.temp_dir_alice.name
        self.temp_dir_bob = tempfile.TemporaryDirectory()
        self.bob_dir_path = self.temp_dir_bob.name

    def set_up_alice(self):
        print("Setting up Alice")
        self.alice_gpg = gnupg.GPG(gnupghome=self.alice_dir_path)
        self.alice_input_data = self.alice_gpg.gen_key_input(**create_key_input_dict(key_reference_dict, alice_key_vals_dict))
        self.alice_gpg.gen_key(self.alice_input_data)
        self.alice_key = self.alice_gpg.list_keys()[0]
        self.alice_export = self.alice_gpg.export_keys(self.alice_key['keyid'])

    def set_up_bob(self):
        print("Setting up Bob")
        self.bob_gpg = gnupg.GPG(gnupghome=self.bob_dir_path)
        self.bob_input_data = self.bob_gpg.gen_key_input(**create_key_input_dict(key_reference_dict, bob_key_vals_dict))
        self.bob_gpg.gen_key(self.bob_input_data)
        self.bob_key = self.bob_gpg.list_keys()[0]
        self.bob_export = self.bob_gpg.export_keys(self.bob_key['keyid'])

    def set_up_alice_and_bob(self):
        self.set_up_alice()
        self.set_up_bob()
        self.alice_gpg.import_keys(str(self.bob_export))
        self.bob_gpg.import_keys(str(self.alice_export))

    def __del__(self):
        self.temp_dir_alice.cleanup()
        self.temp_dir_bob.cleanup()