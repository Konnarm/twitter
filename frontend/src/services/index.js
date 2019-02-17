import axios from 'axios';

export function getFollowers(handle, slice) {
    return axios.request({
        method: 'GET',
        url: slice ? `/followers/get_followers/${handle}/${slice}/` : `/followers/get_followers/${handle}/`,
        baseURL: 'http://localhost:8000',
    })
}
