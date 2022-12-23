import QtQuick
import QtQuick.Controls

Rectangle {
    id: element

    color: MyStyle.general.color

    //width: MyStyle.element.width
    radius: MyStyle.element.radius
    anchors.margins: MyStyle.element.margins

    implicitHeight: mouseArea.implicitHeight

    property alias text: elementText.text
    property alias textColor: elementText.color
    property alias textBold: elementText.font.bold
    property alias textSize: elementText.font.pointSize
    property alias textCenter: elementText.horizontalAlignment
    property bool creationDateVisible: false
    property bool dueDateVisible: false
    property alias creationDateText: creationDate.text
    property alias dueDateText: dueDate.text
    property alias completionDateText: completionDate.text
    property bool isTaskCompleted: false
    property bool isTaskDue: false
    property bool isClosable: true
    property bool isCompletable: true
    property Item dragTarget
    property int dragAxis
    property real dragMinimumX
    property real dragMinimumY
    property real dragMaximumX
    property real dragMaximumY

    signal close
    signal complete
    signal creationDateChanged
    signal dueDateChanged
    signal completionDateChanged
    
    property bool elementHovered: {
        if(mouseArea.containsMouse || elementText.hovered || closeButton.hovered || completeButton.hovered)
        {
            true
        } else
        {
            false
        }
    }

    function isValidDate(d) {
        if(Date.fromLocaleDateString(Qt.locale("de_DE"), d, "d.M.yyyy") != "Invalid Date")
        {
            return true
        } else {
            return false
        }
    }

    MouseArea {
        id: mouseArea

        anchors.fill: parent
        implicitHeight: {
            if(element.creationDateVisible)
            {
                creationDate.implicitHeight + elementText.implicitHeight + 2 * MyStyle.element.margins
            } else {
                elementText.implicitHeight + 2 * MyStyle.element.margins
            }
        }

        hoverEnabled: true
        preventStealing: true
        
        drag.target: element.dragTarget
        drag.axis: element.dragAxis
        drag.minimumX: element.dragMinimumX
        drag.minimumY: element.dragMinimumY
        drag.maximumX: element.dragMaximumX
        drag.maximumY: element.dragMaximumY

        TextArea {
            id: elementText

            background: Rectangle {
                color: MyStyle.general.color
            }
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: MyStyle.element.margins

            hoverEnabled: true

            wrapMode: Text.Wrap
            clip: true

            font.strikeout: element.isTaskCompleted
        }
        TextField {
            id: creationDate

            anchors.top: elementText.bottom
            anchors.left: parent.left
            anchors.leftMargin: MyStyle.element.margins

            width: contentWidth + leftPadding + rightPadding
            background: Rectangle {
                border.color: "transparent"
            }

            color: elementText.color
            font.pointSize: elementText.font.pointSize - 2

            hoverEnabled: true

            visible: element.creationDateVisible

            maximumLength: 10
            validator: RegularExpressionValidator { regularExpression: /[0-9.]+/ }

            onTextChanged: {
                if(element.isValidDate(text))
                {
                    element.creationDateChanged();
                    color = elementText.color;
                }
                else  {
                    color = "red";
                }
            }
            MyToolTip {
                text: "Startdatum"
            }
        }
        TextField {
            id: dueDate

            anchors.top: elementText.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            
            width: contentWidth + leftPadding + rightPadding
            background: Rectangle {
                border.color: "transparent"
            }

            color: elementText.color
            Binding on color {
                when: element.isTaskDue
                value: "red"
            }
            font.pointSize: elementText.font.pointSize - 2

            hoverEnabled: true

            visible: element.dueDateVisible

            maximumLength: 10
            validator: RegularExpressionValidator { regularExpression: /[0-9.]+/ }

            onTextChanged: {
                if(element.isValidDate(text)) {
                    element.dueDateChanged();
                    if(element.isTaskDue) {
                        color = "red";
                    }
                    else {
                        color = elementText.color;
                    }
                }
                else  {
                    color = "blueviolet";
                }
            }

            MyToolTip {
                text: "Fälligkeitsdatum"
            }
        }
        TextField {
            id: completionDate

            anchors.top: elementText.bottom
            anchors.right: parent.right
            anchors.rightMargin: MyStyle.element.margins
            
            width: contentWidth + leftPadding + rightPadding
            background: Rectangle {
                border.color: "transparent"
            }

            color: elementText.color
            font.pointSize: elementText.font.pointSize - 2

            hoverEnabled: true

            visible: element.isTaskCompleted

            maximumLength: 10
            validator: RegularExpressionValidator { regularExpression: /[0-9.]+/ }

            onTextChanged: {
                if(element.isValidDate(text)) {
                    element.completionDateChanged()
                    color = elementText.color;
                }
                else  {
                    color = "red";
                }
            }
            MyToolTip {
                text: "Enddatum"
            }
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

        visible: {
            if(element.elementHovered && element.isClosable)
            {
                true
            }
            else{
                false
            }
        }

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

        visible: {
            if(element.elementHovered && element.isCompletable)
            {
                true
            }
            else{
                false
            }
        }

        HoverHandler {
        }

        onClicked: element.complete()
    }
}