import papermill as pm
from pathlib import Path
import json
import argparse

TRACE_DIR = './traces'
REF_DIR = './test_ref'
ENDPOINT = 'http://zenflows-debug.interfacer.dyne.org/api'
NB_FILE = 'IFServices.ipynb'

NOT_COMPARABLE = ['id', 'trackingIdentifier',
                  'hasPointInTime', 'hasBeginning', 'hasEnd']

params = [
    {
        "positional": ['-e', '--endpoint'],
        "params": {
            "dest": 'endpoint',
            "action": 'store',
            "default": ENDPOINT,
            "help": 'specifies the endpoint to talk to'
        }
    },
    {
        "positional": ['-n', '--nb_file'],
        "params":{
            "dest": 'nb_file',
            "action": 'store',
            "default": NB_FILE,
            "help": 'specifies the full path to the notebook'
        }
    },
    {
        "positional": ['-p', '--present'],
        "params":{
            "dest": 'present',
            "action": 'store_true',
            "help": 'specifies whether the trace has already been calculated'
        }
    }
]

cmp_nodes_verbose = False
def cmp_nodes(ref_dpp, new_dpp, prt=False):
    """
        This function performs the comparison
        between a node from the reference trace
        and a node of the generated trace.
        Some fields (contained in NOT_COMPARABLE)
        are excluded as they change at every run.
    """
    # Compare nodes that are not dictionaries
    if type(ref_dpp) is not dict:
        if not ref_dpp == new_dpp:
            if cmp_nodes_verbose:
                print(f'Values {ref_dpp} and {new_dpp} differ')
            return False
        else:
            return True

    # Compare nodes that are dictionaries
    for key in ref_dpp.keys():
        if key in NOT_COMPARABLE:
            continue
        elif type(ref_dpp[key]) is dict:
            if not cmp_nodes(ref_dpp[key], new_dpp[key]):
                if cmp_nodes_verbose:
                    print(f'Dict {key} is diffent')
                return False
        elif type(ref_dpp[key]) is list:
            # find corresponding items to compare
            for ref_item in ref_dpp[key]:
                found = False
                for new_item in new_dpp[key]:
                    if cmp_nodes(ref_item, new_item):
                        found = True
                        break
                if not found:
                    if cmp_nodes_verbose:
                        print(f'Item {ref_item} is not in new trace')
                    return False
        elif ref_dpp[key] != new_dpp[key]:
            if cmp_nodes_verbose:
                print(f'Key {key} is diffent: {ref_dpp[key]} != {new_dpp[key]}')
            return False
    return True


def cmp_traces_rec(ref_dpp, new_dpp):
    """
        This function recursively examines
        children nodes
    """
    # We try to find corresponding children
    for ref_child in ref_dpp['children']:
        found = False
        for new_child in new_dpp['children']:
            if cmp_nodes(ref_child, new_child):
                found = True
                if not cmp_traces_rec(ref_child, new_child):
                    return False
                break
        # Corresponding children not found
        if not found:
            print(
                f"{ref_dpp['name']} and {new_dpp['name']} have diffent children")
            return False

    return True


def cmp_traces(ref_dpp, new_dpp):
    """
        This function calls the function to
        compare the root node and then the
        function that recursively compares
        children nodes
    """
    if not cmp_nodes(ref_dpp, new_dpp):
        print(f"{ref_dpp['name']} and {new_dpp['name']} are different")
        return False

    return cmp_traces_rec(ref_dpp, new_dpp)


def test_dpp(nb_file, endpoint, present):
    """
        This function runs the notebook if present==False,
        (meaning the trace file is already available)
        reads the generated trace file and the reference one,
        and passes them to the function that performs the comparison
    """
    # breakpoint()
    parameters = pm.inspect_notebook(nb_file)
    exp_name = parameters['USE_CASE']['default'].replace("'", "")

    if not present:
        pm.execute_notebook(nb_file, '/dev/null',
                            parameters=dict(ENDPOINT=endpoint))

    trace_file = f'{exp_name}_fe_trace.json'

    file_to_read = Path(REF_DIR, trace_file)
    with open(file_to_read, 'r') as f:
        ref_dpp = json.loads(f.read())
        ref_dpp = ref_dpp[0]

    file_to_read = Path(TRACE_DIR, trace_file)
    with open(file_to_read, 'r') as f:
        new_dpp = json.loads(f.read())
        new_dpp = new_dpp[0]

    if cmp_traces(ref_dpp, new_dpp):
        print("verification passed")
        assert 1
    else:
        print("verification NOT passed")
        assert 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # breakpoint()
    for argmt in params:
        parser.add_argument(*argmt['positional'], **argmt['params'])

    args, unknown = parser.parse_known_args()

    test_dpp(args.nb_file, args.endpoint, args.present)
