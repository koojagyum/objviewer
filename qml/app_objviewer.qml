import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.2

import ObjViewer 1.0

import '.'

Item {
    width: 720 + 200
    height: 720

    SplitView {
        orientation: Qt.Horizontal
        anchors.fill: parent

        Rectangle {
            Layout.minimumWidth: 200
            Layout.maximumWidth: 200

            Column {
                x: 10; y: 10
                width: parent.width - x * 2
                spacing: 10

                Button {
                    text: 'Load obj...'
                    onClicked: {
                        fileDialog.selectExisting = true
                        fileDialog.fileDialogType = 1
                        fileDialog.visible = true
                    }
                }
                HDivider {}

                Button {
                    text: 'Reset Camera'
                    enabled: false
                }
            }

            FileDialog {
                id: fileDialog
                visible: false
                title: 'File browser'
                folder: '../objviewer'
                selectExisting: false

                property var fileDialogType: 0

                onAccepted: {
                    switch (fileDialogType) {
                    case 0: // none
                        break
                    case 1: // open source image file
                        objview.objSource = fileDialog.fileUrl
                        break
                    default:
                        break
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            color: 'gray'

            ObjView {
                id: objview
                anchors.fill: parent
            }
        }
    }
}
