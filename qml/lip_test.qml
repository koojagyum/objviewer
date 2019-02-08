import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2

import FaceWarp 1.0


Item {
    width: 700+200
    height: 400

    SplitView {
        orientation: Qt.Horizontal
        anchors.fill: parent

        Rectangle {
            id: contentpanel

            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                anchors.fill: parent

                LiveFaceView {
                    id: faceview
                    anchors.fill: parent
                    play: true
                }

                Text {
                    anchors {
                        bottom: parent.bottom
                        horizontalCenter: parent.horizontalCenter
                        bottomMargin: 20
                    }
                    text: 'LipTest view'
                    color: 'gray'
                }
            }
        }

        Rectangle {
            id: rightpanel

            Layout.preferredWidth: 200
            Layout.maximumWidth: 240
            Layout.minimumWidth: 200
            Layout.fillWidth: false
            Layout.fillHeight: true

            color: 'ivory'
        }

    }
}
