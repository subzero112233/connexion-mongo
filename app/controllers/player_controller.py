import logging
import connexion

from models.player import Player

logger = logging.getLogger(__name__)


def create_one():
    body = connexion.request.get_json()
    res = Player.create_one(body)
    if not res:
        return {"error": "Player: '{}' already exists in the database".format(body['name'])}, 409

    return {"success": True}, 201


def delete_one(name):
    name = connexion.request.args.to_dict()['name']
    res = Player.delete_one(name)
    if res.deleted_count == 0:
        return {"error": "Player: '{}' not found".format(name)}, 404

    return {"success": True}, 200


def get_many(result_from, size, sort):
    players, total = Player.get_many(result_from, size, sort)
    return {"results": players, "total": total, "result_from": result_from, "result_size": len(players)}, 201


def get_one():
    name = connexion.request.args.to_dict()['name']
    res = Player.get_one(name)
    if not res:
        return {"error": "Player: '{}' not found".format(name)}, 404

    return res, 200


def update_one():
    body = connexion.request.get_json()
    res = Player.update_one(body)
    if not res:
        return {"error": "Player: '{}' not found".format(body['name'])}, 404

    return {"success": True}, 200


def health_check():  # pragma: no cover
    return {"success": True}, 200