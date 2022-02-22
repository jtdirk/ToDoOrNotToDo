pragma Singleton
import QtQuick

QtObject {
    property QtObject element: QtObject {
        property int width: 200
        property int height: 50
        property int radius: 10
        property int margins: 5
    }

    property QtObject project: QtObject {
        property color color: "black"
        property int textSize: 10
        property QtObject border: QtObject {
            property int width: 3
        }
    }

    property QtObject task: QtObject {
        property color color: "grey"
        property int textSize: 9
        property QtObject border: QtObject {
            property int width: 2
        }
    }
}
