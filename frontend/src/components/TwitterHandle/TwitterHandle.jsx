import React, {Component} from "react";
import {connect} from "react-redux";
import {updateFollowers, updateFollowersWebsocket} from "../../actions/index";
import Pusher from 'pusher-js';

class SearchInput extends Component {
    constructor() {
        super();
        this.state = {
            handle: "",
            followersSlice: 0
        };
        this.handleTwitterHandleChange = this.handleTwitterHandleChange.bind(this);
        this.handleSliceChange = this.handleSliceChange.bind(this);

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleTwitterHandleChange(event) {
        this.setState({handle: event.target.value})
    }

    handleSliceChange(event) {
        this.setState({followersSlice: event.target.value})
    }

    handleSubmit(event) {
        event.preventDefault();
        this.props.dispatch(updateFollowers(this.state.handle, this.state.slice));
        if (this.channel !== undefined) {
            this.channel.unbind();

            this.pusher.unsubscribe(this.channel.name);
            this.channel = undefined;
        }
        if (this.channel === undefined) {
            this.channel = this.pusher.subscribe(this.state.handle);
            this.channel.bind('followers_update', data => this.props.dispatch(updateFollowersWebsocket(data)));
        }

    }

    componentWillUnmount() {
        this.channel.unbind();

        this.pusher.unsubscribe(this.channel);
    }

    componentDidMount() {
        this.pusher = new Pusher(process.env.REACT_APP_PUSHER_API_KEY, {
            cluster: 'eu',
            forceTLS: true
        });
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                Twitter Handle
                <input type={"text"} name="handle" value={this.state.handle}
                       onChange={this.handleTwitterHandleChange.bind(this)}/>
                Followers slice(optional: 0 to process all followers, 1 or more to fetch data for first or more followers)
                <input type={"number"} name="slice" value={this.state.followersSlice}
                       onChange={this.handleSliceChange.bind(this)}/>
                <input type="submit" value="Find"/>

            </form>
        );
    }
}

export function mapDispatchToProps(dispatch) {
    return {
        dispatch,
    };
}

export default connect(null, mapDispatchToProps)(SearchInput);
