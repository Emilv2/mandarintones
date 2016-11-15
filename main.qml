import QtQuick 2.5
import QtQuick.Window 2.2
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import QtCharts 2.0

ApplicationWindow {

    visible: true
    width: 640
    height: 480
    title: qsTr("Mandarin Tones")
    menuBar: MenuBar {
        id: menubar
        Menu {
            title: "File"
            MenuItem {
                id: startTest
                text: "New Test"
                onTriggered: {
                    view.state = "TEST"
                    this.enabled = false
                    stopTest.enabled = true
                }
            }

            MenuItem {
                id: stopTest
                text: "Stop Test"
                enabled: false
                onTriggered: {
                    view.state = "NORMAL"
                    this.enabled = false
                    startTest.enabled = true
                }
            }

            MenuItem {
                text: "Exit"
            }
        }

        Menu {
            title: "Tools"
            MenuItem {
                text: "Statistics"
                onTriggered: {
                    view.state = "STATISTICS"
                }
            }
            MenuItem {
                text: "Settings"
            }
        }

        Menu {
            title: "Help"
            MenuItem {
                text: "About"
            }
        }
    }

    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label {
                text: "Read Only"
            }
        }
    }

    Rectangle {
        id: view
        anchors.fill: parent
        state: "NORMAL"

        states: [
            State {
                name: "NORMAL"
                PropertyChanges {
                    target: test
                    visible: false
                }
                PropertyChanges {
                    target: normal
                    visible: true
                }
                PropertyChanges {
                    target: statistics
                    visible: false
                }
            },
            State {
                name: "TEST"
                PropertyChanges {
                    target: test
                    visible: true
                }
                PropertyChanges {
                    target: normal
                    visible: false
                }
                PropertyChanges {
                    target: statistics
                    visible: false
                }
            },
            State {
                name: "STATISTICS"
                PropertyChanges {
                    target: test
                    visible: false
                }
                PropertyChanges {
                    target: normal
                    visible: false
                }
                PropertyChanges {
                    target: statistics
                    visible: true
                }
            }
        ]

        Rectangle {
            id: test
            visible: false
            anchors.fill: parent

            TextField {
                placeholderText: qsTr("Enter your answer here")
            }

            Button {
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }
                text: "New Game"
                onClicked: console.log("This doesn't do anything yet...")
            }
        }

        Rectangle {
            id: normal
            visible: true
            anchors.fill: parent
            Label {
                text: "Normal Mode"
            }
        }

        Rectangle {
            id: statistics
            visible: false
            anchors.fill: parent

            ColumnLayout{
                anchors.fill: parent
                Column {
                    anchors.fill: parent

                    Label {
                        text: "Statistics come here"
                    }

                    GroupBox {
                        title: "Select timewindow"

                        RowLayout {
                            ExclusiveGroup {
                                id: tabPositionGroup
                            }
                            RadioButton {
                                text: "Day"
                                checked: true
                                exclusiveGroup: tabPositionGroup
                            }
                            RadioButton {
                                text: "Week"
                                exclusiveGroup: tabPositionGroup
                            }
                            RadioButton {
                                text: "Month"
                                exclusiveGroup: tabPositionGroup
                            }
                            RadioButton {
                                text: "All Time"
                                exclusiveGroup: tabPositionGroup
                            }
                        }
                    }
                }

                    ChartView {
                        title: "Bar series"
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        //legend.alignment: Qt.AlignBottom
                        antialiasing: true
                        

                        BarSeries {
                            id: mySeries
                            
                            axisX: BarCategoryAxis { categories: ["2007", "2008", "2009", "2010", "2011", "2012" ] }
                            BarSet { label: "Bob"; values: [2, 2, 3, 4, 5, 6] }
                            BarSet { label: "Susan"; values: [5, 1, 2, 4, 1, 7] }
                            BarSet { label: "James"; values: [3, 5, 8, 13, 5, 8] }
                        }
                    }

            }
        }
    }
}
