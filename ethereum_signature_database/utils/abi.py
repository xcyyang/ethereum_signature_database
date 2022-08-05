from sha3 import keccak_256

# sanity check we are using the right sha3 function
assert (
    keccak_256(b"").hexdigest()
    == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
), keccak_256(
    b"",
).hexdigest()  # NOQA


def make_4byte_signature(text_signature: str) -> bytes:
    from .encoding import force_bytes

    return keccak_256(force_bytes(text_signature)).digest()[:4]


# ARGUMENT_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "name": {
#             "type": "string",
#         },
#         "type": {
#             "type": "string",
#         },
#         "components": {
#             "type": "array",
#             "items": {"$ref": "#/definitions/argument"},
#         },
#     },
#     "required": ["name", "type"],
# }


# NAME = {"type": "string"}
# BOOLEAN = {"type": "boolean"}
# INPUTS = OUTPUTS = {"type": "array", "items": {"$ref": "#/definitions/argument"}}
# EVENT_TYPE = {"type": "string", "enum": ["event"]}
# CONSTRUCTOR_TYPE = {"type": "string", "enum": ["constructor"]}

# EVENT_ARGUMENT_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "name": NAME,
#         "type": NAME,
#         "indexed": BOOLEAN,
#     },
#     "required": ["name", "type", "indexed"],
# }

# FUNCTION_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "type": {"type": "string", "enum": ["function", "receive"]},
#         "inputs": INPUTS,
#         "outputs": OUTPUTS,
#         "name": NAME,
#         "stateMutability": {
#             "type": "string",
#             "enum": ["pure", "view", "nonpayable", "payable"],
#         },
#     },
#     "required": ["type", "inputs", "outputs", "name"],
#     "definitions": {
#         "argument": ARGUMENT_SCHEMA,
#     },
# }

# FALLBACK_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "type": {"type": "string", "enum": ["fallback"]},
#         "stateMutability": {
#             "type": "string",
#             "enum": ["pure", "view", "nonpayable", "payable"],
#         },
#     },
#     "required": ["type"],
#     "definitions": {
#         "argument": ARGUMENT_SCHEMA,
#     },
# }

# EVENT_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "anonymous": BOOLEAN,
#         "type": {"type": "string", "enum": ["event"]},
#         "inputs": {
#             "type": "array",
#             "items": EVENT_ARGUMENT_SCHEMA,
#         },
#         "name": NAME,
#     },
#     "required": ["type", "inputs", "name"],
# }

# CONSTRUCTOR_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "type": {"type": "string", "enum": ["constructor"]},
#         "inputs": INPUTS,
#         "stateMutability": {
#             "type": "string",
#             "enum": ["pure", "view", "nonpayable", "payable"],
#         },
#     },
#     "required": ["type", "inputs"],
#     "definitions": {
#         "argument": ARGUMENT_SCHEMA,
#     },
# }

# CONTRACT_ABI_SCHEMA = {
#     "type": "array",
#     "items": {
#         "anyOf": [
#             {"$ref": "#/definitions/fallback"},
#             {"$ref": "#/definitions/function"},
#             {"$ref": "#/definitions/event"},
#             {"$ref": "#/definitions/constructor"},
#         ],
#     },
#     "definitions": {
#         "function": FUNCTION_SCHEMA,
#         "event": EVENT_SCHEMA,
#         "constructor": CONSTRUCTOR_SCHEMA,
#         "argument": ARGUMENT_SCHEMA,
#         "fallback": FALLBACK_SCHEMA,
#     },
# }


# def validate_contract_abi(contract_abi) -> None:
#     validate(contract_abi, CONTRACT_ABI_SCHEMA)


# def is_valid_contract_abi(contract_abi) -> bool:
#     try:
#         validate_contract_abi(contract_abi)
#     except ValidationError:
#         return False
#     else:
#         return True


# def function_definition_to_text_signature(abi: Dict[str, Any]) -> str:
#     return "{fn_name}({fn_input_types})".format(
#         fn_name=abi["name"],
#         fn_input_types=",".join(
#             [collapse_if_tuple(abi_input) for abi_input in abi.get("inputs", [])],
#         ),
#     )


# def event_definition_to_text_signature(abi: Dict[str, Any]) -> str:
#     return "{fn_name}({fn_input_types})".format(
#         fn_name=abi["name"],
#         fn_input_types=",".join(
#             [
#                 f"{collapse_if_tuple(abi_input)}{' indexed' if abi_input['indexed'] else ''}"
#                 for abi_input in abi.get("inputs", [])
#             ],
#         ),
#     )
