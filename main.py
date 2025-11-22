from flask import Flask, jsonify, request
from check_service import CheckService
from maps_service import TravelModeSelector
from custom_exceptions import CheckPointAlreadyExistsError, CheckpointNotFoundError, NoTargetsFoundError, InvalidTravelModeError
app = Flask(__name__)


@app.route('/home')
def home():
    return jsonify({'message': 'Welcome TrailMe home'})


@app.route('/checkpoint/add', methods=['POST'])
def add_checkpoint():
    data = request.json

    if not data or not all(i in data for i in ('label', 'image', 'latitude', 'longitude')):
        return ({'message': 'Bad request'}), 400

    check_service = CheckService(label=data['label'],
                                 image=data['image'],
                                 latitude=data['latitude'],
                                 longitude=data['longitude'])

    try:
        check_service.add_checkpoint()
        return jsonify({'message': 'Resource created'}), 201

    except CheckPointAlreadyExistsError:
        return jsonify({'message': 'Checkpoint already exists'}), 200

    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


@app.route('/checkpoint/update', methods=['PUT'])
def update_checkpoint():
    data = request.json

    if not data or not all(i in data for i in ('id', 'label', 'image', 'latitude', 'longitude')):
        return ({'message': 'Bad'}), 400

    check_service = CheckService(id=data['id'],
                                 label=data['label'],
                                 image=data['image'],
                                 latitude=data['latitude'],
                                 longitude=data['longitude'])

    try:
        check_service.update_checkpoint()
        return jsonify({'message': 'Resource updated'}), 200

    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


@app.route('/checkpoint/<int:id>', methods=['DELETE'])
def delete_checkpoint(id):
    check_service = CheckService(id=id)
    try:
        check_service.delete_checkpoint()
        return jsonify({'message': 'Checkpoint deleted'}), 200
    except CheckpointNotFoundError as e:
        return jsonify({'message': f'Error: {e}'}), 404
    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


@app.route('/checkpoint', methods=['GET'])
def get_checkpoints():
    check_service = CheckService(id=id)
    try:
        checkpoints = check_service.get_checkpoints()
        return jsonify({'message': checkpoints}), 200
    except NoTargetsFoundError as e:
        return jsonify({'message': f'Error: {e}'}), 404
    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


@app.route('/checkpoint/get-trip-details', methods=['POST'])
def get_trip_details():
    data = request.json
    if not data or not all(i in data for i in ('id', 'olat', 'olong', 'travel_mode')):
        return jsonify({'message': 'Bad request'}), 400
    check_service = CheckService(id=data['id'])
    try:
        co_ordinates = check_service.get_checkpoint()
    except CheckpointNotFoundError as e:
        return jsonify({'message': f'Error: {e}'}), 404
    travel_selector = TravelModeSelector(
        olat=data['olat'], olong=data['olong'], dlat=co_ordinates['lat'], dlong=co_ordinates['long'], travel_type=data['travel_mode'])
    try:
        trip_details = travel_selector.travel_details()
        return jsonify({'message': trip_details}), 200
    except InvalidTravelModeError as e:
        return jsonify({'message': f'Error: {e}'})
    except InvalidTravelModeError as e:
        return jsonify({'message': f'Error: {e}'}), 400
    except Exception as e:
        return jsonify({'message': f'Server error: {e}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
