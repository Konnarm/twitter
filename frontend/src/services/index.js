import axios from 'axios';

export function getFollowers(handle, slice) {
    return axios.request({
        method: 'GET',
        url: slice ? `/followers/get_followers/${handle}/${slice}/` : `/followers/get_followers/${handle}/`,
        baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'https://followersoffollowers.herokuapp.com',
    })
}
