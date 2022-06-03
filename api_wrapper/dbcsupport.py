from pydantic import BaseModel


def pre(x: dict, model_body: dict) -> bool:
    """ Pre-condition """
    for k, v in model_body.items():
        if k not in x:
            return False

        if isinstance(x[k], dict):
            return pre(x[k], model_body[k])

        if not isinstance(x[k], v):
            return False

    return True


def post(result: any, model_final: dict) -> bool:
    """ Post-condition """
    for k, v in model_final.items():
        _dict = result.dict() if isinstance(result, BaseModel) else result
        if k not in _dict:
            return False

        if isinstance(_dict.get(k), dict):
            return post(_dict.get(k), model_final[k])

        if not isinstance(_dict.get(k), v.type):
            return False

        if isinstance(_dict.get(k), str) and v.len is not None:
            if len(_dict.get(k)) != v.len:
                return False

    return True


def inv(this: any, model_final: dict) -> bool:
    """ Invariant """
    return post(this, model_final)
