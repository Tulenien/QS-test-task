from citygrid import *

if __name__ == "__main__":
    cityGrid = CityGrid(10, 10, 30)
    towers = cityGrid.positionTowers(1, [], 0)
    print(*towers)
    cityGrid.print_pseudo()
    cityGrid.plot(towers)
