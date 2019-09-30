from PySide2.QtWidgets import QLabel, QDockWidget, QTextEdit
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QSize
import main

class AsciiTableWidget(QDockWidget):
    
    def __init__(self):
        super(AsciiTableWidget, self).__init__()
        self.edit = QTextEdit()
        self.edit.setReadOnly(True)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setMinimumWidth(200)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.edit.insertHtml("""<table class="table table-ascii table-bordered table-border-ascii table-hover table-xs page-break">
            <thead>
            <tr class="table-header">
                <th class="col-plus"></th>
                <th class="col-40px">DEC</th>
                <th class="col-40px">OCT</th>
                <th class="col-40px">HEX</th>
                <th class="col-80px">BIN</th>
                <th class="col-50px">Symbol</th>
                <th class="col-110px">HTML Number</th>
                <th class="col-html">HTML Name</th>
                <th class="col-description" align="left">Description</th>
            </tr>
            </thead>
            <tbody>
            <tr><td></td><td>0</td><td>000</td><td>00</td><td>00000000</td><td>NUL</td><td>&amp;#000;</td><td>&nbsp;</td><td>Null char</td></tr>
            <tr><td></td><td>1</td><td>001</td><td>01</td><td>00000001</td><td>SOH</td><td>&amp;#001;</td><td>&nbsp;</td><td>Start of Heading</td></tr>
            <tr><td></td><td>2</td><td>002</td><td>02</td><td>00000010</td><td>STX</td><td>&amp;#002;</td><td>&nbsp;</td><td>Start of Text</td></tr>
            <tr><td></td><td>3</td><td>003</td><td>03</td><td>00000011</td><td>ETX</td><td>&amp;#003;</td><td>&nbsp;</td><td>End of Text</td></tr>
            <tr><td></td><td>4</td><td>004</td><td>04</td><td>00000100</td><td>EOT</td><td>&amp;#004;</td><td>&nbsp;</td><td>End of Transmission</td></tr>
            <tr><td></td><td>5</td><td>005</td><td>05</td><td>00000101</td><td>ENQ</td><td>&amp;#005;</td><td>&nbsp;</td><td>Enquiry</td></tr>
            <tr><td></td><td>6</td><td>006</td><td>06</td><td>00000110</td><td>ACK</td><td>&amp;#006;</td><td>&nbsp;</td><td>Acknowledgment</td></tr>
            <tr><td></td><td>7</td><td>007</td><td>07</td><td>00000111</td><td>BEL</td><td>&amp;#007;</td><td>&nbsp;</td><td>Bell</td></tr>
            <tr><td></td><td>8</td><td>010</td><td>08</td><td>00001000</td><td> BS</td><td>&amp;#008;</td><td>&nbsp;</td><td>Back Space</td></tr>
            <tr><td></td><td>9</td><td>011</td><td>09</td><td>00001001</td><td> HT</td><td>&amp;#009;</td><td>&nbsp;</td><td>Horizontal Tab</td></tr>
            <tr><td></td><td>10</td><td>012</td><td>0A</td><td>00001010</td><td> LF</td><td>&amp;#010;</td><td>&nbsp;</td><td>Line Feed</td></tr>
            <tr><td></td><td>11</td><td>013</td><td>0B</td><td>00001011</td><td> VT</td><td>&amp;#011;</td><td>&nbsp;</td><td>Vertical Tab</td></tr>
            <tr><td></td><td>12</td><td>014</td><td>0C</td><td>00001100</td><td> FF</td><td>&amp;#012;</td><td>&nbsp;</td><td>Form Feed</td></tr>
            <tr><td></td><td>13</td><td>015</td><td>0D</td><td>00001101</td><td> CR</td><td>&amp;#013;</td><td>&nbsp;</td><td>Carriage Return</td></tr>
            <tr><td></td><td>14</td><td>016</td><td>0E</td><td>00001110</td><td> SO</td><td>&amp;#014;</td><td>&nbsp;</td><td>Shift Out / X-On</td></tr>
            <tr><td></td><td>15</td><td>017</td><td>0F</td><td>00001111</td><td> SI</td><td>&amp;#015;</td><td>&nbsp;</td><td>Shift In / X-Off</td></tr>
            <tr><td></td><td>16</td><td>020</td><td>10</td><td>00010000</td><td>DLE</td><td>&amp;#016;</td><td>&nbsp;</td><td>Data Line Escape</td></tr>
            <tr><td></td><td>17</td><td>021</td><td>11</td><td>00010001</td><td>DC1</td><td>&amp;#017;</td><td>&nbsp;</td><td>Device Control 1 (oft. XON)</td></tr>
            <tr><td></td><td>18</td><td>022</td><td>12</td><td>00010010</td><td>DC2</td><td>&amp;#018;</td><td>&nbsp;</td><td>Device Control 2</td></tr>
            <tr><td></td><td>19</td><td>023</td><td>13</td><td>00010011</td><td>DC3</td><td>&amp;#019;</td><td>&nbsp;</td><td>Device Control 3 (oft. XOFF)</td></tr>
            <tr><td></td><td>20</td><td>024</td><td>14</td><td>00010100</td><td>DC4</td><td>&amp;#020;</td><td>&nbsp;</td><td>Device Control 4</td></tr>
            <tr><td></td><td>21</td><td>025</td><td>15</td><td>00010101</td><td>NAK</td><td>&amp;#021;</td><td>&nbsp;</td><td>Negative Acknowledgement</td></tr>
            <tr><td></td><td>22</td><td>026</td><td>16</td><td>00010110</td><td>SYN</td><td>&amp;#022;</td><td>&nbsp;</td><td>Synchronous Idle</td></tr>
            <tr><td></td><td>23</td><td>027</td><td>17</td><td>00010111</td><td>ETB</td><td>&amp;#023;</td><td>&nbsp;</td><td>End of Transmit Block</td></tr>
            <tr><td></td><td>24</td><td>030</td><td>18</td><td>00011000</td><td>CAN</td><td>&amp;#024;</td><td>&nbsp;</td><td>Cancel</td></tr>
            <tr><td></td><td>25</td><td>031</td><td>19</td><td>00011001</td><td> EM</td><td>&amp;#025;</td><td>&nbsp;</td><td>End of Medium</td></tr>
            <tr><td></td><td>26</td><td>032</td><td>1A</td><td>00011010</td><td>SUB</td><td>&amp;#026;</td><td>&nbsp;</td><td>Substitute</td></tr>
            <tr><td></td><td>27</td><td>033</td><td>1B</td><td>00011011</td><td>ESC</td><td>&amp;#027;</td><td>&nbsp;</td><td>Escape</td></tr>
            <tr><td></td><td>28</td><td>034</td><td>1C</td><td>00011100</td><td> FS</td><td>&amp;#028;</td><td>&nbsp;</td><td>File Separator</td></tr>
            <tr><td></td><td>29</td><td>035</td><td>1D</td><td>00011101</td><td> GS</td><td>&amp;#029;</td><td>&nbsp;</td><td>Group Separator</td></tr>
            <tr><td></td><td>30</td><td>036</td><td>1E</td><td>00011110</td><td> RS</td><td>&amp;#030;</td><td>&nbsp;</td><td>Record Separator</td></tr>
            <tr><td></td><td>31</td><td>037</td><td>1F</td><td>00011111</td><td> US</td><td>&amp;#031;</td><td>&nbsp;</td><td>Unit Separator</td></tr>
            </tbody>
        </table>""")
        self.setWidget(self.edit)