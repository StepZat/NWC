import random
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView
import copy
aCost = []
aSupply = []
aDemand = []
n = 0
m = 0
nVeryLargeNumber = 99999999999
aRoute = []
aDual = []
aSigma = []
PivotN = -1
PivotM = -1


def generateOddRandom():
    odd_random_array = []
    for item in range(0, 3):
        odd_random_array.append(random.randint(1, 20))
    odd_random_array.sort()
    return ",".join(map(str, odd_random_array))


class NWC(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_values = None
        self.random_button = None
        self.size_button = None
        self.buyer_input = None
        self.buyer_label = None
        self.seller_input = None
        self.seller_label = None
        self.input_label = None
        self.type_selector_button = None
        self.type_selector_label = None
        self.title_label = None
        self.layout_matrix = None
        self.layout_1_2 = None
        self.layout_1_1 = None
        self.layout_1_0 = None
        self.grid_2 = None
        self.layout_2 = None
        self.layout_1 = None
        self.costs = None
        self.plans = None
        self.isSellerEmpty = False
        self.isBuyerEmpty = False
        self.grid = None
        self.layout = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Метод северо-западного угла')
        self.setMaximumWidth(1570)
        self.layout_1 = QtWidgets.QVBoxLayout()
        self.layout_2 = QtWidgets.QVBoxLayout()
        self.layout_1_0 = QtWidgets.QHBoxLayout()
        self.layout_1_1 = QtWidgets.QHBoxLayout()
        self.layout_1_2 = QtWidgets.QHBoxLayout()
        self.layout_matrix = QtWidgets.QGridLayout()
        self.grid_2 = QtWidgets.QGridLayout()
        self.grid = QtWidgets.QGridLayout()
        self.grid.addLayout(self.layout_1, 0, 0)
        self.grid.addLayout(self.layout_2, 0, 1)
        self.setLayout(self.grid)

        # Название программы в главном окне
        self.title_label = QtWidgets.QLabel()
        self.title_label.setText(
            "Программа для расчета опорного плана транспортной задачи методом северо-западного угла")

        # Выбор режима работы - нечеткая или четкая логика
        self.type_selector_label = QtWidgets.QLabel("Выберите, если нужен режим нечеткой логики")
        self.type_selector_button = QtWidgets.QRadioButton()

        # Ввод количества поставщиков и ппотребителей - название
        self.input_label = QtWidgets.QLabel()
        self.input_label.setText("Введите количество поставщиков и потребителей:")

        # Название - поставщики
        self.seller_label = QtWidgets.QLabel()
        self.seller_label.setText("Поставщики")

        # Ввод количества поставщиков
        self.seller_input = QtWidgets.QSpinBox()
        self.seller_input.setMinimum(1)
        self.seller_input.setMaximum(10)

        # Название - потребители
        self.buyer_label = QtWidgets.QLabel()
        self.buyer_label.setText("Потребители")

        # Ввод количества потребителей
        self.buyer_input = QtWidgets.QSpinBox()
        self.buyer_input.setMinimum(1)
        self.buyer_input.setMaximum(10)

        # Кнопка - установить размеры
        self.size_button = QtWidgets.QPushButton()
        self.size_button.setText("Установить размеры")

        # Кнопка - удалить заданные значения размеров
        self.random_button = QtWidgets.QPushButton()
        self.random_button.setText("Заполнить случайными числами")
        self.random_button.setEnabled(False)

        self.setup_values = QtWidgets.QPushButton()
        self.setup_values.setText("Рассчитать")
        self.setup_values.setEnabled(False)

        self.layout_1.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout_1.addWidget(self.input_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_1.addLayout(self.layout_1_0)
        self.layout_1_0.addWidget(self.type_selector_label)
        self.layout_1_0.addWidget(self.type_selector_button)
        self.layout_1.addLayout(self.layout_1_1)
        self.layout_1_1.addWidget(self.seller_label)
        self.layout_1_1.addWidget(self.seller_input)
        self.layout_1_1.addWidget(self.buyer_label)
        self.layout_1_1.addWidget(self.buyer_input)
        self.layout_1.addLayout(self.layout_1_2)
        self.layout_1_2.addWidget(self.size_button)
        self.layout_1_2.addWidget(self.random_button)
        self.layout_1_2.addWidget(self.setup_values)
        self.size_button.clicked.connect(self.button_clicked)
        self.setup_values.clicked.connect(self.button_setup)
        self.show()

    def prepare_weights(self, evenLogic: bool):
        self.weight_matrix = QtWidgets.QTableWidget()
        self.weight_matrix.setColumnCount(self.buyer_input.value() + 1)
        self.weight_matrix.setRowCount(self.seller_input.value() + 1)
        self.weight_matrix.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.weight_matrix.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.weight_matrix.setMaximumSize(self.getQTableWidgetSizeWeight())
        self.weight_matrix.setMinimumSize(self.getQTableWidgetSizeWeight())
        self.weight_matrix.setSelectionMode(QAbstractItemView.NoSelection)
        self.weight_matrix.setHorizontalHeaderItem(self.buyer_input.value(), QTableWidgetItem("Поставщики"))
        self.weight_matrix.setVerticalHeaderItem(self.seller_input.value(), QTableWidgetItem("Потребители"))
        if evenLogic is True:
            for item_i in range(self.weight_matrix.rowCount()-1):
                for item_j in range(self.weight_matrix.columnCount()-1):
                    self.weight_matrix.setItem(item_i, item_j, QTableWidgetItem("0,0,0"))
            for item_i in range(self.weight_matrix.rowCount()-1):
                self.weight_matrix.setItem(item_i, self.weight_matrix.columnCount()-1, QTableWidgetItem("0"))
            for item_j in range(self.weight_matrix.columnCount()-1):
                self.weight_matrix.setItem(self.weight_matrix.rowCount()-1, item_j, QTableWidgetItem("0"))
        else:
            for item_i in range(self.weight_matrix.rowCount()):
                for item_j in range(self.weight_matrix.columnCount()):
                    self.weight_matrix.setItem(item_i, item_j, QTableWidgetItem("0"))
        self.weight_matrix.setItem(self.seller_input.value(), self.buyer_input.value(), QTableWidgetItem(""))
        self.weight_matrix.item(self.seller_input.value(), self.buyer_input.value()).setBackground(Qt.lightGray)
        self.weight_matrix.item(self.seller_input.value(), self.buyer_input.value()).setFlags(Qt.ItemIsSelectable)
        self.layout_matrix.addWidget(self.weight_matrix, 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout_1.addLayout(self.layout_matrix)
        self.setup_values.setEnabled(True)
        param = self.type_selector_button.isChecked()
        self.random_button.clicked.connect(lambda: self.randomSetup(param))
        self.random_button.setEnabled(True)
        self.layout_1.addStretch()
        self.adjustSize()



    def button_clicked(self):
        # Матрица весов
        if not hasattr(self, 'weight_matrix') and not hasattr(self, 'scrollarea'):
            self.prepare_weights(self.type_selector_button.isChecked())
        elif hasattr(self, 'weight_matrix') and not hasattr(self, 'scrollarea'):
            self.weight_matrix.setParent(None)
            self.layout_1.removeWidget(self.weight_matrix)
            self.weight_matrix.deleteLater()
            QApplication.processEvents()
            delattr(self, 'weight_matrix')
            self.prepare_weights(self.type_selector_button.isChecked())
        elif hasattr(self, 'weight_matrix') and hasattr(self, 'scrollarea'):
            self.weight_matrix.setParent(None)
            self.layout_1.removeWidget(self.weight_matrix)
            self.weight_matrix.deleteLater()
            self.scrollarea.setParent(None)
            self.layout_2.removeWidget(self.scrollarea)
            self.scrollarea.deleteLater()
            QApplication.processEvents()
            delattr(self, 'weight_matrix')
            delattr(self, 'scrollarea')
            self.prepare_weights(self.type_selector_button.isChecked())

    def random_setup_layout(self):
        self.count_setup()
        self.scrollarea = QtWidgets.QScrollArea(self)
        self.scrollarea.setFixedHeight(800)
        self.scrollarea.setMinimumWidth(400)
        self.scrollarea.setMaximumWidth(700)
        self.scrollarea.setWidgetResizable(True)
        widget = QtWidgets.QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QtWidgets.QVBoxLayout(widget)
        for item in range(1, len(self.costs) + 1):
            self.result_matrix_label = QtWidgets.QLabel()
            self.result_matrix_label.setText(f"Шаг: {item}, стоимость: {self.costs[item]} ")
            self.result_matrix_label.setFixedHeight(50)
            self.layout_SArea.addWidget(self.result_matrix_label)
            self.result_matrix = QtWidgets.QTableWidget()
            self.result_matrix.setColumnCount(self.buyer_input.value())
            self.result_matrix.setRowCount(self.seller_input.value())
            self.result_matrix.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.result_matrix.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.result_matrix.setMaximumSize(self.getQTableWidgetSizeReady())
            self.result_matrix.setMinimumSize(self.getQTableWidgetSizeReady())
            self.result_matrix.setSelectionMode(QAbstractItemView.NoSelection)
            for item_i in range(self.result_matrix.rowCount()):
                for item_j in range(self.result_matrix.columnCount()):
                    self.result_matrix.setItem(item_i, item_j,
                                               QTableWidgetItem(str(self.plans[item][item_i][item_j])))
            self.layout_SArea.addWidget(self.result_matrix)
        self.scrollarea.setFixedWidth(self.layout_SArea.sizeHint().width() + 30)
        self.layout_2.addWidget(self.scrollarea)

    def button_setup(self):
        if not hasattr(self, 'scrollarea'):
            self.random_setup_layout()
        else:
            self.scrollarea.setParent(None)
            self.layout_2.removeWidget(self.scrollarea)
            self.scrollarea.deleteLater()
            QApplication.processEvents()
            delattr(self, 'scrollarea')
            self.random_setup_layout()

    def count_setup(self):
        global aCost
        global aSupply
        global aDemand
        global n, m
        global aRoute
        global aSigma
        global PivotM, PivotN
        global aDual
        if self.type_selector_button.isChecked():
            aCost = [[list(map(int, self.weight_matrix.item(i, j).text().split(","))) 
                      for j in range(self.buyer_input.value())] for i in range(self.seller_input.value())]
            aSupply = [int(self.weight_matrix.item(i, self.buyer_input.value()).text()) for i in
                       range(self.seller_input.value())]
            aDemand = [int(self.weight_matrix.item(self.seller_input.value(), j).text()) for j in
                       range(self.buyer_input.value())]
            self.plans = {}
            self.costs = {}
            n = len(aSupply)
            m = len(aDemand)
            aRoute = []
            for x in range(n):
                aRoute.append([0] * m)
            aSigma = []
            for x in range(n):
                aSigma.append([-1] * m)
            NorthWest()
            PivotN = -1
            PivotM = -1
            flag = 1
            arr_copy = copy.deepcopy(aRoute)
            self.plans[flag] = arr_copy
            self.costs[flag] = countSigma(arr_copy)
            while self.NotOptimalFuzzy():
                BetterOptimal()
                flag += 1
                arr_copy = copy.deepcopy(aRoute)
                self.costs[flag] = countSigma(arr_copy)
                self.plans[flag] = arr_copy
        else:
            aCost = [[int(self.weight_matrix.item(i, j).text()) for j in range(self.buyer_input.value())] for i in
                     range(self.seller_input.value())]
            aSupply = [int(self.weight_matrix.item(i, self.buyer_input.value()).text()) for i in
                       range(self.seller_input.value())]
            aDemand = [int(self.weight_matrix.item(self.seller_input.value(), j).text()) for j in
                       range(self.buyer_input.value())]
            self.plans = {}
            self.costs = {}
            n = len(aSupply)
            m = len(aDemand)
            aRoute = []
            for x in range(n):
                aRoute.append([0] * m)
            aDual = []
            for x in range(n):
                aDual.append([-1] * m)
            NorthWest()
            PivotN = -1
            PivotM = -1
            PrintOut()
            flag = 1
            arr_copy = copy.deepcopy(aRoute)
            self.plans[flag] = arr_copy
            self.costs[flag] = PrintOut()
            while NotOptimal():
                BetterOptimal()
                flag += 1
                arr_copy = copy.deepcopy(aRoute)
                self.costs[flag] = PrintOut()
                self.plans[flag] = arr_copy

    def getQTableWidgetSizeSellers(self):
        w = 50
        h = self.table_sellers.horizontalHeader().height()
        for i in range(self.table_sellers.rowCount()):
            h += self.table_sellers.rowHeight(i)
        return QtCore.QSize(w, h)

    def getQTableWidgetSizeBuyers(self):
        w = 30
        for i in range(self.table_buyers.columnCount()):
            self.table_buyers.setColumnWidth(i, 50)
            w += self.table_buyers.columnWidth(i)
        h = 50
        return QtCore.QSize(w, h)

    def getQTableWidgetSizeWeight(self):
        w = 100
        for i in range(self.weight_matrix.columnCount()-1):
            self.weight_matrix.setColumnWidth(i, 80)
            w += self.weight_matrix.columnWidth(i)
        w += 180
        h = self.weight_matrix.horizontalHeader().height()
        for i in range(self.weight_matrix.rowCount()):
            h += self.weight_matrix.rowHeight(i)
        return QtCore.QSize(w, h)

    def getQTableWidgetSizeReady(self):
        w = 30
        for i in range(self.result_matrix.columnCount()):
            self.result_matrix.setColumnWidth(i, 50)
            w += self.result_matrix.columnWidth(i)

        h = self.result_matrix.horizontalHeader().height()
        for i in range(self.result_matrix.rowCount()):
            h += self.result_matrix.rowHeight(i)
        return QtCore.QSize(w, h)

    def checkIsNumber(self):
        for itemRow in range(self.weight_matrix.rowCount()):
            for itemColumn in range(self.weight_matrix.columnCount()):
                if self.weight_matrix.item(itemRow, itemColumn).flags() & QtCore.Qt.ItemFlag.ItemIsEditable:
                    if not self.weight_matrix.item(itemRow, itemColumn).text().isnumeric():
                        QtWidgets.QMessageBox.about(self, "Ошибка!", "Введите числа во всех ячейках!")
                        return False
        return True

    def randomSetup(self, evenLogic: bool):
        for itemRow in range(self.weight_matrix.rowCount()-1):
            for itemColumn in range(self.weight_matrix.columnCount()-1):
                if evenLogic is True:
                    self.weight_matrix.setItem(itemRow, itemColumn, QTableWidgetItem(generateOddRandom()))
                else:
                    self.weight_matrix.setItem(itemRow, itemColumn, QTableWidgetItem(str(random.randint(1, 20))))
        sellers_random = []
        buyers_random = []
        for i in range(self.weight_matrix.rowCount() - 1):
            sellers_random.append(random.randint(1, 200))
        for i in range(self.weight_matrix.columnCount() - 1):
            buyers_random.append(random.randint(1, 200))
        while sum(sellers_random) != sum(buyers_random):
            buyers_random = []
            for i in range(self.weight_matrix.columnCount() - 1):
                buyers_random.append(random.randint(1, 200))
        sellers_random.sort()
        buyers_random.sort()
        for i in range(self.weight_matrix.rowCount()-1):
            self.weight_matrix.setItem(i, self.weight_matrix.columnCount()-1, QTableWidgetItem(str(sellers_random[i])))
        for j in range(self.weight_matrix.columnCount()-1):
            self.weight_matrix.setItem(self.weight_matrix.rowCount()-1, j, QTableWidgetItem(str(buyers_random[j])))

    def NotOptimalFuzzy(self):
        global PivotN
        global PivotM
        xMin = list(self.costs.values())[-1]
        GetSigma()
        for u in range(0, n):
            for v in range(0, m):
                x = aSigma[u][v]
                if x < xMin and x != -1:
                    xMin = x
                    PivotN = u
                    PivotM = v
        return xMin != list(self.costs.values())[-1]


def countSigma(route):
    temp1 = 0
    temp2 = 0
    temp3 = 0
    for x in range(n):
        for y in range(m):
            temp1 += aCost[x][y][0] * route[x][y]
            temp2 += aCost[x][y][1] * route[x][y]
            temp3 += aCost[x][y][2] * route[x][y]
    sigma = (temp1+2*temp2+temp3)//2
    return sigma


def PrintOut():
    nCost = 0
    for x in range(n):
        for y in range(m):
            nCost += aCost[x][y] * aRoute[x][y]
    return nCost
        

def NorthWest():
    global aRoute
    u = 0
    v = 0
    aS = [0] * m
    aD = [0] * n
    while u <= n - 1 and v <= m - 1:
        if aDemand[v] - aS[v] < aSupply[u] - aD[u]:
            z = aDemand[v] - aS[v]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            v += 1
        else:
            z = aSupply[u] - aD[u]
            aRoute[u][v] = z
            aS[v] += z
            aD[u] += z
            u += 1


def GetSigma():
    global aSigma
    for u in range(0, n):
        for v in range(0, m):
            nMin = nVeryLargeNumber
            route_copy = copy.deepcopy(aRoute)
            aSigma[u][v] = -1  # null value
            if route_copy[u][v] == 0:
                aPath = FindPath(u, v)
                for w in range(1, len(aPath), 2):
                    t = route_copy[aPath[w][0]][aPath[w][1]]
                    if t < nMin:
                        nMin = t
                for w in range(1, len(aPath), 2):
                    route_copy[aPath[w][0]][aPath[w][1]] -= nMin
                    route_copy[aPath[w - 1][0]][aPath[w - 1][1]] += nMin
                sigma = countSigma(route_copy)
                aSigma[u][v] = sigma


def NotOptimal():
    global PivotN
    global PivotM
    nMax = -nVeryLargeNumber
    GetDual()
    for u in range(0, n):
        for v in range(0, m):
            x = aDual[u][v]
            if x > nMax:
                nMax = x
                PivotN = u
                PivotM = v
    return nMax > 0


def GetDual():
    global aDual
    for u in range(0, n):
        for v in range(0, m):
            aDual[u][v] = -0.5  # null value
            if aRoute[u][v] == 0:
                aPath = FindPath(u, v)
                z = -1
                x = 0
                for w in aPath:
                    x += z * aCost[w[0]][w[1]]
                    z *= -1
                aDual[u][v] = x


def FindPath(u, v):
    aPath = [[u, v]]
    if not LookHorizontaly(aPath, u, v, u, v):
        return aPath
    return aPath


def LookHorizontaly(aPath, u, v, u1, v1):
    for i in range(0, m):
        if i != v and aRoute[u][i] != 0:
            if i == v1:
                aPath.append([u, i])
                return True
            if LookVerticaly(aPath, u, i, u1, v1):
                aPath.append([u, i])
                return True
    return False


def LookVerticaly(aPath, u, v, u1, v1):
    for i in range(0, n):
        if i != u and aRoute[i][v] != 0:
            if LookHorizontaly(aPath, i, v, u1, v1):
                aPath.append([i, v])
                return True
    return False


def BetterOptimal():
    global aRoute
    aPath = FindPath(PivotN, PivotM)
    nMin = nVeryLargeNumber
    for w in range(1, len(aPath), 2):
        t = aRoute[aPath[w][0]][aPath[w][1]]
        if t < nMin:
            nMin = t
    for w in range(1, len(aPath), 2):
        aRoute[aPath[w][0]][aPath[w][1]] -= nMin
        aRoute[aPath[w - 1][0]][aPath[w - 1][1]] += nMin


def main():
    app = QApplication(sys.argv)
    ex = NWC()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
