import os
from paraview import simple
from paraview.web import protocols as pv_protocols
from wslink import register as exportRpc


class ParaViewWebCinemaReader(pv_protocols.ParaViewWebProtocol):
    def __init__(self, baseDir=None, **kwargs):
        super(ParaViewWebCinemaReader, self).__init__()
        self.setBaseDirectory(baseDir)
        self.currentIndex = -1
        self.currentFileName = ''
        self.databasePath = ''

    @exportRpc("pv.cinema.load.database")
    def loadCinemaDatabase(self, cdbPath):
        validPath = self.getAbsolutePath(cdbPath)
        if not os.path.isdir(validPath):
            return {'success': False,
                    'reason': 'Not a valid database. Should be a .cdb directory'}
        for entry in os.listdir(validPath):
            validEntry = os.path.join(validPath, entry)
            if os.path.isfile(validEntry):
                (r, extension) = os.path.splitext(entry)
                if extension == '.csv':
                    self.databasePath = validEntry
                    return self.loadCinemaFile(1)

    @exportRpc("pv.cinema.load.file")
    def loadCinemaFile(self, index):
        import csv
        with open(self.databasePath) as csvfile:
            cinemaReader = csv.reader(csvfile, delimiter=',')
            lineNumber = 0
            pathIdx = 0
            for row in cinemaReader:
                if lineNumber == 0:
                    pathIdx = row.index('FILE')
                elif lineNumber == index:
                    self.currentIndex = index
                    directory = os.path.dirname(self.databasePath)
                    self.currentFileName = row[pathIdx]
                    filePath = os.path.join(directory, self.currentFileName)
                    reader = simple.OpenDataFile(filePath)
                    simple.HideAll()
                    simple.Delete()

                    readerDisplay = simple.Show(reader)
                    simple.ColorBy(readerDisplay, ('POINTS', 'CriticalType') )
                    renderView1 = simple.GetActiveView()
                    readerDisplay.RescaleTransferFunctionToDataRange(True, False)
                    readerDisplay.SetScalarBarVisibility(renderView1, True)
                    readerDisplay.RenderLinesAsTubes = 1
                    readerDisplay.LineWidth = 2

                    # create pass array filter to display points
                    passArrays1 = simple.PassArrays(registrationName='PassArrays1', Input=reader)
                    passArrays1Display = simple.Show()
                    passArrays1Display.SetRepresentationType('Point Gaussian')

                    # set scalar coloring
                    simple.ColorBy(passArrays1Display, None)

                    simple.ResetCamera()
                    simple.Render()
                    if self.getApplication():
                        self.getApplication().InvokeEvent('UpdateEvent')

                    return {'success': True, 'id': reader.GetGlobalIDAsString()}

                lineNumber += 1

    @exportRpc("pv.cinema.current")
    def getCurrentInfo(self):
        return {'name': self.currentFileName, 'id': self.currentIndex}

    @exportRpc("pv.cinema.databasesize")
    def getNumberOfDataset(self):
        import csv
        with open(self.databasePath) as csvfile:
            cinemaReader = csv.reader(csvfile, delimiter=',')
            return {'size': sum(1 for row in cinemaReader) - 1}
        return {'size': 0}
