"""
helpers.py	

helper object and functions for setting up gpg test keys

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

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
