import {getFollowers} from '../services'

import {UPDATE_FOLLOWERS} from "../constants/actions-types";

export function updateFollowers(handle, slice) {
    return dispatch => getFollowers(handle, slice).then(response => dispatch(success(response.data.followers)));

    function success(payload) {
        return {type: UPDATE_FOLLOWERS, payload};
    }
}
