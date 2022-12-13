# Reece Williams (Reece#3370) | December 2022
# Easily get a changelog for a Cosmos SDK Upgrade proposal text.

from gh_logic import get_prs_output
from util import get_env
import os

UPGRADE_NAME = get_env("UPGRADE_NAME")
CHAIN_NAME = get_env("CHAIN_NAME")
BLOCK_HEIGHT = get_env("BLOCK_HEIGHT")

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
proposal_folder = os.path.join(root_dir, "proposals")
os.makedirs(proposal_folder, exist_ok=True)

SUMMARY = f"""
This is a proposal to set the {CHAIN_NAME} {UPGRADE_NAME} upgrade at block height {BLOCK_HEIGHT}. Juno v12 is an feature rich upgrade including the following new modules:\n
- x/Oracle Module
- x/FeeShare Module
- x/TokenFactory Module
- x/GlobalFee Module

The above modules have been tested both on other Networks (uume, evmos, osmosis, and gaia respectively), on the Juno Testnet (uni-5), and our own newly added test end-2-end suite.

This update also includes the following updates:\n
- Interchain Account Controller
- CosmWasm 0.30.0
- IBC v4.2.0 + IBCFees
- 20% minimum gov deposit (prevents phishing attack spam)
"""

VOTING = f"""
## Voting\n
By voting YES on this proposal, you agree that the {CHAIN_NAME} {UPGRADE_NAME} upgrade should proceed.\n
By voting NO on this proposal, you disagree that the {CHAIN_NAME} {UPGRADE_NAME} upgrade should happen.\n
By voting NO WITH VETO, you disagree with the {UPGRADE_NAME} upgrade taking place, and additionally wish to see depositors penalized.\n
By voting ABSTAIN, you decline to give an opinion on the upgrade.\n
"""



technical_details = get_prs_output(show_body=False, ignore_dependabot=True)

# save all of these things in a file

proposal_text = f"""# {CHAIN_NAME} {UPGRADE_NAME} Upgrade Proposal
## Summary\n{SUMMARY}\n<br>\n
## Technical Details & Changes\n{technical_details}\n\n
\n<br>\n{VOTING}\n"""

# save to markdown file for viewing
with open(os.path.join(proposal_folder, f"{UPGRADE_NAME}.md"), "w") as f:
    f.write(proposal_text)


res = input("Enter 'yes' if the markdown is correct to create the copy pasted proposal (y/n):")
if res.lower().startswith("y"):    
    # replace proposal_text new lines to the \n character
    res = proposal_text.replace("\n", "\\n")
    res = res.replace("'", "\\'")
    res = res.replace('"', '\\"')
    print("="*20)

    if res.startswith("\\n"):
        res = res[2:]
    if res.endswith("\\n"):
        res = res[:-2]

    # print(res)
    # save output to file
    fName = f"{UPGRADE_NAME}_proposal.txt"
    with open(os.path.join(proposal_folder, fName), "w") as f:
        f.write(res)
        print(f"Saved to file {fName}")