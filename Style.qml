pragma Singleton
import QtQuick

QtObject {
    property QtObject general: QtObject {
        property color color: "white"
        property real scale: 1
    }

    property QtObject element: QtObject {
        property int width: 200 * MyStyle.general.scale
        property int height: 50 * MyStyle.general.scale
        property int radius: 10 * MyStyle.general.scale
        property int margins: 5 * MyStyle.general.scale
    }

    property QtObject project: QtObject {
        property color color: "black"
        property int textSize: 10 * MyStyle.general.scale
        property QtObject border: QtObject {
            property int width: 3 * MyStyle.general.scale
        }
    }

    property QtObject task: QtObject {
        property color color: "gray"
        property int textSize: 9 * MyStyle.general.scale
        property QtObject border: QtObject {
            property int width: 2 * MyStyle.general.scale
        }
    }
}
