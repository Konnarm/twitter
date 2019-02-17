import React, {Component} from "react";
import {connect} from "react-redux";
import {updateFollowers} from "../../actions/index";

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
        event.preventDefault()
        debugger
        this.props.dispatch(updateFollowers(this.state.handle, this.state.slice))
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                Twitter Handle
                <input type={"text"} name="handle" value={this.state.handle}
                       onChange={this.handleTwitterHandleChange.bind(this)}/>
                Followers slice(optional)
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
