import {UPDATE_FOLLOWERS} from "../constants/actions-types";
import {Map} from 'immutable'

const initialState = Map({followers: Map()});

function rootReducer(state = initialState, action) {
    switch (action.type) {
        case UPDATE_FOLLOWERS:
            return state.set('followers', Map(action.payload));
        default:
            return state;
    }
}

export default rootReducer;
