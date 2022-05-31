from pydantic import BaseModel


def pre(x: dict, model_body: dict) -> bool:
    for k, v in model_body.items():
        if k not in x:
            return False

        if isinstance(x[k], dict):
            return pre(x[k], model_body[k])

        if not isinstance(x[k], v):
            return False

    return True


def post(result: dict, model_final: dict) -> bool:
    for k, v in model_final.items():
        if k not in model_final:
            return False

        _dict = result.dict() if isinstance(result, BaseModel) else result

        if isinstance(_dict.get(k), dict):
            return post(_dict.get(k), model_final[k])

        if not isinstance(_dict.get(k), v):
            return False

    return True


def inv(this: any, model_final: dict) -> bool:
    return post(this, model_final)
