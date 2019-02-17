import React, {Component} from "react";
import Followers from "./Followers/Followers";
import SearchInput from "./TwitterHandle/TwitterHandle";


class App extends Component {
    render() {
        return (
            <div className="row mt-5">
                <div className="col-md-4 offset-md-1">
                    <h2>Provide twitter handle</h2>
                    <SearchInput/>
                </div>
                <div className="col-md-4 offset-md-1">
                    <h2>Followers of followers</h2>
                    <Followers/>
                </div>
            </div>
        );
    }
}

export default App;
