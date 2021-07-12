from mml.mutations import *
true_predicate = lambda sample, state: True



function_table = {
    '_ZN6google8protobuf8internal12kEmptyStringE': [ 'libprotobuf-8.dll' ],
    '??_V@YAXPEAX@Z': [ 'msvcrt.dll, MSVCR100.dll, MSVCR110.dll, MSVCR120.dll' ],
    'EventActivityIdControl': [ 'api-ms-win-eventing-provider-l1-1-0.dll' ],
    '??0exception@@QEAA@AEBQEBD@Z': [ 'msvcrt.dll' ],
    '??0exception@@QEAA@XZ': [ 'msvcrt.dll' ],
    'CloseThreadpoolWork': [ 'api-ms-win-core-threadpool-l1-2-0.dll' ],
    '_ZTVN6google8protobuf8internal16FunctionClosure0E': [ 'libprotobuf-8.dll' ],
    '_o__cexit': [ 'api-ms-win-crt-private-l1-1-0.dll' ],
    '_o__initialize_onexit_table': [ 'api-ms-win-crt-private-l1-1-0.dll' ],
    '_o__crt_atexit': [ 'api-ms-win-crt-private-l1-1-0.dll' ],
    '_o__register_onexit_function': [ 'api-ms-win-crt-private-l1-1-0.dll' ],
    '_o_free': [ 'api-ms-win-crt-private-l1-1-0.dll' ],
    'Cla$init': [ 'c5runx.dll', 'c60runx.dll', 'ClaRUN.dll' ],
    '_o___stdio_common_vswprintf':  [ 'api-ms-win-crt-private-l1-1-0.dll' ]
}

dlls = [
    'msvcrt.dll',
    'MSVCR100.dll',
    'MSVCR110.dll',
    'MSVCR120.dll',
    'libprotobuf-8.dll',
    'api-ms-win-eventing-provider-l1-1-0.dll',
    'api-ms-win-core-threadpool-l1-2-0.dll',
    'api-ms-win-crt-private-l1-1-0.dll',
    'c5runx.dll', 'c60runx.dll', 'ClaRUN.dll'
]

max_strings = 30
add_string_wsize_every = 5
max_entropy_changes = 25
change_entropy_wsize_every = 3
max_removed_strings = 10

mutations_table = {
    0: { 
        'predicate': lambda sample, state: (state['added_strings'] < max_strings and state['added_strings'] % add_string_wsize_every != 0 ) , 
        'mutation': AddStringMutation(0) 
    },
    1: {
        'predicate': lambda sample, state: (state['added_strings'] < max_strings and state['added_strings'] % add_string_wsize_every == 0 ),
        'mutation': AddStringWithSizeMutation(30, 1)
    },
    2: {
        'predicate': lambda sample, state: (state['entropy_changes'] < max_entropy_changes and state['entropy_changes'] % change_entropy_wsize_every != 0 ),
        'mutation': ChangeStringEntropyMutation(5.595417, 0.3, 2)
    },
    3: {
        'predicate': lambda sample, state: (state['entropy_changes'] < max_entropy_changes and state['entropy_changes'] % change_entropy_wsize_every == 0 ),
        'mutation': ChangeStringEntropyWithSizeMutation(5.595417, 0.5, 35, 3)
    },
    4: {
        'predicate': lambda sample, state: (state['removed_strings'] < max_removed_strings),
        'mutation': RemoveStringMutation(4)
    },
    5: {
        'predicate': true_predicate,
        'mutation': AddSectionMutation(512, 5)
    },
    6: {
        'predicate': true_predicate,
        'mutation': AddBytesMutation(128, 6)
    },
    7: {
        'predicate': true_predicate,
        'mutation': AddCodeBytesMutation(64, 7)
    },
    8: {
        'predicate': lambda sample, state: (state['added_libs'] < 14),
        'mutation': ImportFunctionMutation(function_table, 8)
    },
    9: {
        'predicate': true_predicate,
        'mutation': ChangeTimestampMutation(1332756000, 1000, 9)
    },
    10: {
        'predicate': lambda sample, state: (sample['has_debug'] == '1'),
        'mutation': RemoveDebugMutation(10)
    },
    11: {
        'predicate': lambda sample, state: (sample['has_signature'] == '0'),
        'mutation': ChangeSignatureMutation(True, 11)
    }
}

"""
This is the same table as above, but all mutations are always allowed to be applied.
"""
always_true_table = {
    0: { 
        'predicate': true_predicate , 
        'mutation': AddStringMutation(0) 
    },
    1: {
        'predicate': true_predicate,
        'mutation': AddStringWithSizeMutation(30, 1)
    },
    2: {
        'predicate': true_predicate,
        'mutation': ChangeStringEntropyMutation(5.595417, 0.3, 2)
    },
    3: {
        'predicate': true_predicate,
        'mutation': ChangeStringEntropyWithSizeMutation(5.595417, 0.5, 35, 3)
    },
    4: {
        'predicate': true_predicate,
        'mutation': RemoveStringMutation(4)
    },
    5: {
        'predicate': true_predicate,
        'mutation': AddSectionMutation(512, 5)
    },
    6: {
        'predicate': true_predicate,
        'mutation': AddBytesMutation(128, 6)
    },
    7: {
        'predicate': true_predicate,
        'mutation': AddCodeBytesMutation(64, 7)
    },
    8: {
        'predicate': true_predicate,
        'mutation': ImportFunctionMutation(function_table, 8)
    },
    9: {
        'predicate': true_predicate,
        'mutation': ChangeTimestampMutation(1332756000, 1000, 9)
    },
    10: {
        'predicate': true_predicate,
        'mutation': RemoveDebugMutation(10)
    },
    11: {
        'predicate': true_predicate,
        'mutation': ChangeSignatureMutation(True, 11)
    }
}