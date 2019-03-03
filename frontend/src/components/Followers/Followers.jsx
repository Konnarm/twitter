import React, {Component} from "react";
import {connect} from "react-redux";

class Followers extends Component {
    render() {
        let followers = [];
        this.props.followers.map((el, key) =>
            followers.push(<li className="list-group-item" key={key}>
                {key}: {el}
            </li>)
        );
        return (
            <ul className="list-group list-group-flush">
                {followers}
            </ul>
        );
    }
}

const mapStateToProps = state => {
    return {followers: state.get('followers')};
};

export function mapDispatchToProps(dispatch) {
    return {
        dispatch,
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Followers);

