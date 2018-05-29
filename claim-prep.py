#!/usr/bin/env python3
# Copyright (c) 2018 PrimeVR
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import os
import sys
import argparse

from lib.value_db import ValueDb
from lib.claimed_nuggets import ClaimedNuggets
from lib.report.prep import PrepReport
from lib.tails import check_tails

from lib.options import address_list_arg, not_tails_arg, cache_request_arg
from lib.options import bfc_force_arg
from lib.options import claim_save_file_arg, claim_save_file_arg_validate

###############################################################################
# main
###############################################################################


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Find fork/airdrop balances and prepare claiming "
                    "instructions for a set of provided addresses.")
    claim_save_file_arg(parser)
    address_list_arg(parser)
    not_tails_arg(parser)
    cache_request_arg(parser)
    bfc_force_arg(parser)

    settings = parser.parse_args()
    claim_save_file_arg_validate(settings.claim_save_file)
    tails = not settings.not_tails
    check_tails(tails)

    vdb = ValueDb(settings)

    cn = ClaimedNuggets(settings.claim_save_file)
    cn.update_ids(vdb['nuggets'])
    cn.write()

    vdb['nuggets'].mark_claimed(cn)

    i = PrepReport(vdb)
    i.write()
