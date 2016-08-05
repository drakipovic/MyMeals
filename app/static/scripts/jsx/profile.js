var React = require('react');
var ReactDOM = require('react-dom');
var ReactBSTable = require('react-bootstrap-table');  
var BootstrapTable = ReactBSTable.BootstrapTable;
var TableHeaderColumn = ReactBSTable.TableHeaderColumn;
var DateTimeField = require('react-bootstrap-datetimepicker');


var Meals = React.createClass({
    loadMealsFromServer: function(){
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
    getInitialState: function(){
        return{data: []};
    },
    componentDidMount: function(){
        this.loadMealsFromServer();
        setInterval(this.loadMealsFromServer, 10000);
    },
    handleMealSubmit: function(meal){
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: meal,
            success: function(data){
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err){
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    render: function(){
        return(
            <div className="row">
                <div className="col-md-8 col-lg-8">
                    <MealsTable data={this.state.data} onMealEdit={this.handleMealSubmit} onMealDelete={this.handleMealSubmit} />
                </div>
                <div className="col-md-4 col-lg-4">
                    <MealsForm onMealSubmit={this.handleMealSubmit} />
                </div>
            </div>
        );
    },

});

var MealsForm = React.createClass({
    getInitialState: function(){
        return {'timestamp':'', 'text':'', 'calories':''};
    },
    handleTimestampChange: function(e){
        console.log("newDate", e);
        return this.setState({timestamp: e});
    },
    handleTextChange: function(e){
        this.setState({text: e.target.value});
    },
    handleCaloriesChange: function(e){
        this.setState({calories: e.target.value});
    },
    handleSubmit: function(e){
        e.preventDefault();
        var timestamp = this.state.timestamp;
        var calories = this.state.calories.trim();
        var text = this.state.text.trim();
        if(!text || !calories || !timestamp) return;

        this.props.onMealSubmit({text: text, timestamp: timestamp, calories:calories});
        this.setState({text:'', timestamp:'', calories:''});
    },

    render: function(){
        return(
            <div className="well">
                <form className="form-horizontal" onSubmit={this.handleSubmit}>
                    <fieldset>
                        <legend>Add new meal</legend>
                        <div className="form-group">
                            <div className="col-md-12 col-lg-12">
                                <input
                                    className="form-control"
                                    type="text"
                                    placeholder="Description"
                                    value={this.state.text}
                                    onChange={this.handleTextChange}
                                />
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-md-12 col-lg-12">
                                <input
                                    className="form-control"
                                    type="text"
                                    placeholder="Calories"
                                    value={this.state.calories}
                                    onChange={this.handleCaloriesChange}
                                />
                            </div>
                        </div>
                        <DateTimeField defaultText="Please select a datetime" onChange={this.handleTimestampChange} inputFormat="DD/MM/YY HH:mm"/>
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

var MealsTable = React.createClass({
    onCellEdit: function(row, cellName, cellValue){
        this.props.onMealEdit({text: row.text, timestamp: row.date + ' ' + row.time, calories: row.calories, id: row.id});
    },
    onCellDelete: function(row){
        for(i = 0; i < row.length; ++i){
            this.props.onMealDelete({id: row[i], del: "1"});
        }
    },
    render: function(){
        var cellEditProp = {
            mode: "click",
            blurToSave: true,
            afterSaveCell: this.onCellEdit
        };
        var selectRowProp = {
            mode: "checkbox",
            bgColor: "#1b96fe"
        };
        var options = {
            onDeleteRow: this.onCellDelete,
            clearSearch: true
        };
        return (
            <BootstrapTable options={options} data={this.props.data} pagination={true} cellEdit={cellEditProp} deleteRow={true} selectRow={selectRowProp} search={true} >
                <TableHeaderColumn width="60" dataField="id" isKey={true}>ID</TableHeaderColumn>
                <TableHeaderColumn width="130" dataField="date">Date</TableHeaderColumn>
                <TableHeaderColumn width="80" dataField="time">Time</TableHeaderColumn>
                <TableHeaderColumn dataField="text">Description</TableHeaderColumn>
                <TableHeaderColumn dataField="calories">Calories</TableHeaderColumn>
            </BootstrapTable>
        );
    }
});

function getUrl(){
    var user = window.location.pathname.split("/")[2];
    return "/api/users/" + user;
};

ReactDOM.render(
        <Meals url={getUrl()} />,
        document.getElementById('meals')
);
