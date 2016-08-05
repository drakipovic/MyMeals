var React = require('react');
var ReactDOM = require('react-dom');
var ReactBSTable = require('react-bootstrap-table');  
var BootstrapTable = ReactBSTable.BootstrapTable;
var TableHeaderColumn = ReactBSTable.TableHeaderColumn;


var Users = React.createClass({
    loadUsersFromServer: function(){
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data){
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err){
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    handleUserSubmit: function(user){
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: user,
            success: function(data){
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err){
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    getInitialState: function(){
        return {data: []};
    },

    componentDidMount: function(){
        this.loadUsersFromServer();
        setInterval(this.loadUsersFromServer, 10000);
    },

    onCellEdit: function(row, cellName, cellValue){
        this.handleUserSubmit({username: row.username, id: row.id})
    },
    
    onCellDelete: function(row){
        for(i = 0; i < row.length; ++i){
            this.handleUserSubmit({id: row[i], del: "1"});
        }
    },

    render: function(){
        var selectRowProp = {
            mode: "checkbox",
            bgColor: "#1b96fe"
        };
        var cellEditProp = {
            mode: "click",
            blurToSave: true,
            afterSaveCell: this.onCellEdit
        };
        var options = {
            onDeleteRow: this.onCellDelete,
            clearSearch: true
        };
        return (
            <div className="row">
                <div className="col-md-8 col-lg-8">
                    <BootstrapTable options={options} data={this.state.data} pagination={true} condensed={true} hover={true} deleteRow={true} selectRow={selectRowProp} cellEdit={cellEditProp} search={true}>
                        <TableHeaderColumn dataField="id" isKey={true} width="60">ID</TableHeaderColumn> 
                        <TableHeaderColumn dataField="username">Username</TableHeaderColumn> 
                        <TableHeaderColumn dataField="role" editable={false}>Role</TableHeaderColumn> 
                    </BootstrapTable>
                </div>
                <div className="col-md-4 col-lg-4">
                    <UserForm onUserSubmit={this.handleUserSubmit} />
                </div>
            </div>
        );
    }
});

var UserForm = React.createClass({
    getInitialState: function(){
        return {username: '', password: ''}
    },
    handleUsernameChange: function(e){
        this.setState({username: e.target.value});
    },
    handlePasswordChange: function(e){
        this.setState({password: e.target.value});
    },
    handleSubmit: function(e){
        e.preventDefault();
        var username = this.state.username.trim();
        var password = this.state.password.trim();
        if(!username || !password) return;

        this.props.onUserSubmit({username: username, password: password});
        this.setState({username: '', password: ''});
    },
    render: function(){
        return(
            <div className="well">
                <form className="form-horizontal" onSubmit={this.handleSubmit}>
                    <fieldset>
                        <legend>Add new user</legend>
                        <div className="form-group">
                            <div className="col-md-12 col-lg-12">
                                <input
                                    className="form-control"
                                    type="text"
                                    placeholder="Username"
                                    value={this.state.username}
                                    onChange={this.handleUsernameChange}
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-12 col-lg-12">
                                <input
                                    className="form-control"
                                    type="text"
                                    placeholder="Password"
                                    value={this.state.password}
                                    onChange={this.handlePasswordChange}
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-offset-5 col-lg-offset-5 add-margin">
                                <button type="submit" className="btn btn-primary">Add</button>
                            </div>
                        </div>
                   </fieldset>
                </form>
            </div>
        );
    } 

});

ReactDOM.render(
        <Users url="/api/users" />,
        document.getElementById('users')
);

