from kivy.core.window import Window

from jpype import startJVM, shutdownJVM, getDefaultJVMPath, JClass

from src.ClientWindow import ClientWindow


if __name__ == "__main__":
    Window.maximize()

    resources_path: str = "src\\Resources\\LMClient.jar"

    startJVM(getDefaultJVMPath(), '-ea', f"-Djava.class.path={resources_path}")

    ClientWindow(
        JClass("Client")()
    ).run()

    shutdownJVM()
