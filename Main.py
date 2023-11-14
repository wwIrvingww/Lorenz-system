
import Lorenz_System

if __name__ == '__main__':
    app = Lorenz_System.QApplication(Lorenz_System.sys.argv)
    ex = Lorenz_System.LorenzSystemApp()
    Lorenz_System.sys.exit(app.exec_())
