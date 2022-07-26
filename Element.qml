import QtQuick
import QtQuick.Controls

Rectangle {
    id: element

    width: MyStyle.element.width
    radius: MyStyle.element.radius
    anchors.margins: MyStyle.element.margins

    implicitHeight: mouseArea.implicitHeight

    property alias text: elementText.text
    property alias textColor: elementText.color
    property alias textBold: elementText.font.bold
    property alias textSize: elementText.font.pointSize
    property alias textCenter: elementText.horizontalAlignment
    property bool creationDateVisible: false
    property alias creationDateText: creationDate.text
    property alias completionDateText: completionDate.text
    property bool isTaskCompleted: false
    property bool isClosable: true

    signal close
    signal complete
    
    property bool hovered: {
        if((mouseArea.containsMouse || elementText.hovered || closeButton.hovered) && isClosable)
        {
            true
        } else
        {
            false
        }
    }

    MouseArea {
        id: mouseArea

        anchors.fill: parent
        implicitHeight: {
            if(creationDateVisible)
            {
                creationDate.implicitHeight + elementText.implicitHeight + 2 * MyStyle.element.margins
            } else {
                elementText.implicitHeight + 2 * MyStyle.element.margins
            }
        }

        hoverEnabled: true
        preventStealing: true
        
        TextArea {
            id: elementText

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: MyStyle.element.margins

            hoverEnabled: true

            wrapMode: Text.Wrap
            clip: true

            font.strikeout: isTaskCompleted
        }
        TextInput {
            id: creationDate

            anchors.top: elementText.bottom
            anchors.left: parent.left
            anchors.leftMargin: MyStyle.element.margins

            color: elementText.color
            font.pointSize: elementText.font.pointSize - 2

            visible: creationDateVisible
        }
        TextInput {
            id: completionDate

            anchors.top: elementText.bottom
            anchors.right: parent.right
            anchors.rightMargin: MyStyle.element.margins
            
            color: elementText.color
            font.pointSize: elementText.font.pointSize - 2

            visible: isTaskCompleted
        }
    }
    RoundButton {
        id: closeButton

        width: 20
        height: 20
        radius: 10
        text: "X"
        anchors.top: parent.top
        anchors.right: parent.right

        visible: element.hovered

        HoverHandler {
        }

        onClicked: element.close()
    }
    RoundButton {
        id: completeButton

        width: 20
        height: 20
        radius: 10
        text: "✔"
        anchors.top: parent.top
        anchors.right: closeButton.left

        visible: element.hovered

        HoverHandler {
        }

        onClicked: element.complete()
    }
}