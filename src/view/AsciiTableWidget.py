"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir
    
    This file is part of i386ide.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from PySide2.QtWidgets import QLabel, QDockWidget, QTextEdit
from PySide2.QtGui import QPixmap, QIcon, QTextOption, QTextCursor
from PySide2.QtCore import Qt, QSize
import main

class AsciiTableWidget(QDockWidget):
    
    def __init__(self):
        super(AsciiTableWidget, self).__init__()
        self.edit = QTextEdit()
        self.edit.setReadOnly(True)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setMinimumWidth(200)
        self.label = QLabel("<center>ASCII table</center>")
        self.setTitleBarWidget(self.label)
        self.setWindowTitle("ASCII table")
        self.titleBarWidget().setStyleSheet("background-color: #007ACC;color: white;font-size: 14px;")
        self.edit.setWordWrapMode(QTextOption.NoWrap)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.edit.insertHtml("""
 <table border="1"; width ="100%">
            <thead>
            <tr>
                <th >DEC</th>
                <th >OCT</th>
                <th >HEX</th>
                <th >BIN</th>
                <th>VALUE</th>
            </tr>
            </thead>
            <tbody>

       <tr><td align = "center">0</td><td align = "center">000</td><td align = "center">00</td><td align = "center">00000000</td><td align = "center">NUL</td></tr>
       <tr><td align = "center">1</td><td align = "center">001</td><td align = "center">01</td><td align = "center">00000001</td><td align = "center">SOH</td></tr>
       <tr><td align = "center">2</td><td align = "center">002</td><td align = "center">02</td><td align = "center">00000010</td><td align = "center">STX</td></tr>
       <tr><td align = "center">3</td><td align = "center">003</td><td align = "center">03</td><td align = "center">00000011</td><td align = "center">ETX</td></tr>
       <tr><td align = "center">4</td><td align = "center">004</td><td align = "center">04</td><td align = "center">00000100</td><td align = "center">EOT</td></tr>
       <tr><td align = "center">5</td><td align = "center">005</td><td align = "center">05</td><td align = "center">00000101</td><td align = "center">ENQ</td></tr>
       <tr><td align = "center">6</td><td align = "center">006</td><td align = "center">06</td><td align = "center">00000110</td><td align = "center">ACK</td></tr>
       <tr><td align = "center">7</td><td align = "center">007</td><td align = "center">07</td><td align = "center">00000111</td><td align = "center">BEL</td></tr>
       <tr><td align = "center">8</td><td align = "center">010</td><td align = "center">08</td><td align = "center">00001000</td><td align = "center"> BS</td></tr>
       <tr><td align = "center">9</td><td align = "center">011</td><td align = "center">09</td><td align = "center">00001001</td><td align = "center"> HT</td></tr>
       <tr><td align = "center">10</td><td align = "center">012</td><td align = "center">0A</td><td align = "center">00001010</td><td align = "center"> LF</td></tr>
       <tr><td align = "center">11</td><td align = "center">013</td><td align = "center">0B</td><td align = "center">00001011</td><td align = "center"> VT</td></tr>
       <tr><td align = "center">12</td><td align = "center">014</td><td align = "center">0C</td><td align = "center">00001100</td><td align = "center"> FF</td></tr>
       <tr><td align = "center">13</td><td align = "center">015</td><td align = "center">0D</td><td align = "center">00001101</td><td align = "center"> CR</td></tr>
       <tr><td align = "center">14</td><td align = "center">016</td><td align = "center">0E</td><td align = "center">00001110</td><td align = "center"> SO</td></tr>
       <tr><td align = "center">15</td><td align = "center">017</td><td align = "center">0F</td><td align = "center">00001111</td><td align = "center"> SI</td></tr>
       <tr><td align = "center">16</td><td align = "center">020</td><td align = "center">10</td><td align = "center">00010000</td><td align = "center">DLE</td></tr>
       <tr><td align = "center">17</td><td align = "center">021</td><td align = "center">11</td><td align = "center">00010001</td><td align = "center">DC1</td></tr>
       <tr><td align = "center">18</td><td align = "center">022</td><td align = "center">12</td><td align = "center">00010010</td><td align = "center">DC2</td></tr>
       <tr><td align = "center">19</td><td align = "center">023</td><td align = "center">13</td><td align = "center">00010011</td><td align = "center">DC3</td></tr>
       <tr><td align = "center">20</td><td align = "center">024</td><td align = "center">14</td><td align = "center">00010100</td><td align = "center">DC4</td></tr>
       <tr><td align = "center">21</td><td align = "center">025</td><td align = "center">15</td><td align = "center">00010101</td><td align = "center">NAK</td></tr>
       <tr><td align = "center">22</td><td align = "center">026</td><td align = "center">16</td><td align = "center">00010110</td><td align = "center">SYN</td></tr>
       <tr><td align = "center">23</td><td align = "center">027</td><td align = "center">17</td><td align = "center">00010111</td><td align = "center">ETB</td></tr>
       <tr><td align = "center">24</td><td align = "center">030</td><td align = "center">18</td><td align = "center">00011000</td><td align = "center">CAN</td></tr>
       <tr><td align = "center">25</td><td align = "center">031</td><td align = "center">19</td><td align = "center">00011001</td><td align = "center"> EM</td></tr>
       <tr><td align = "center">26</td><td align = "center">032</td><td align = "center">1A</td><td align = "center">00011010</td><td align = "center">SUB</td></tr>
       <tr><td align = "center">27</td><td align = "center">033</td><td align = "center">1B</td><td align = "center">00011011</td><td align = "center">ESC</td></tr>
       <tr><td align = "center">28</td><td align = "center">034</td><td align = "center">1C</td><td align = "center">00011100</td><td align = "center"> FS</td></tr>
       <tr><td align = "center">29</td><td align = "center">035</td><td align = "center">1D</td><td align = "center">00011101</td><td align = "center"> GS</td></tr>
       <tr><td align = "center">30</td><td align = "center">036</td><td align = "center">1E</td><td align = "center">00011110</td><td align = "center"> RS</td></tr>
       <tr><td align = "center">31</td><td align = "center">037</td><td align = "center">1F</td><td align = "center">00011111</td><td align = "center"> US</td></tr>
       <tr><td align = "center">32</td><td align = "center">040</td><td align = "center">20</td><td align = "center">00100000</td><td align = "center">Space</td></tr>
       <tr><td align = "center">33</td><td align = "center">041</td><td align = "center">21</td><td align = "center">00100001</td><td align = "center">!</td></tr>
       <tr><td align = "center">34</td><td align = "center">042</td><td align = "center">22</td><td align = "center">00100010</td><td align = "center">"</td></tr>
       <tr><td align = "center">35</td><td align = "center">043</td><td align = "center">23</td><td align = "center">00100011</td><td align = "center">#</td></tr>
       <tr><td align = "center">36</td><td align = "center">044</td><td align = "center">24</td><td align = "center">00100100</td><td align = "center">$</td></tr>
       <tr><td align = "center">37</td><td align = "center">045</td><td align = "center">25</td><td align = "center">00100101</td><td align = "center">%</td></tr>
       <tr><td align = "center">38</td><td align = "center">046</td><td align = "center">26</td><td align = "center">00100110</td><td align = "center">&</td></tr>
       <tr><td align = "center">39</td><td align = "center">047</td><td align = "center">27</td><td align = "center">00100111</td><td align = "center">'</td></tr>
       <tr><td align = "center">40</td><td align = "center">050</td><td align = "center">28</td><td align = "center">00101000</td><td align = "center">(</td></tr>
       <tr><td align = "center">41</td><td align = "center">051</td><td align = "center">29</td><td align = "center">00101001</td><td align = "center">)</td></tr>
       <tr><td align = "center">42</td><td align = "center">052</td><td align = "center">2A</td><td align = "center">00101010</td><td align = "center">*</td></tr>
       <tr><td align = "center">43</td><td align = "center">053</td><td align = "center">2B</td><td align = "center">00101011</td><td align = "center">+</td></tr>
       <tr><td align = "center">44</td><td align = "center">054</td><td align = "center">2C</td><td align = "center">00101100</td><td align = "center">,</td></tr>
       <tr><td align = "center">45</td><td align = "center">055</td><td align = "center">2D</td><td align = "center">00101101</td><td align = "center">-</td></tr>
       <tr><td align = "center">46</td><td align = "center">056</td><td align = "center">2E</td><td align = "center">00101110</td><td align = "center">.</td></tr>
       <tr><td align = "center">47</td><td align = "center">057</td><td align = "center">2F</td><td align = "center">00101111</td><td align = "center">/</td></tr>
       <tr><td align = "center">48</td><td align = "center">060</td><td align = "center">30</td><td align = "center">00110000</td><td align = "center">0</td></tr>
       <tr><td align = "center">49</td><td align = "center">061</td><td align = "center">31</td><td align = "center">00110001</td><td align = "center">1</td></tr>
       <tr><td align = "center">50</td><td align = "center">062</td><td align = "center">32</td><td align = "center">00110010</td><td align = "center">2</td></tr>
       <tr><td align = "center">51</td><td align = "center">063</td><td align = "center">33</td><td align = "center">00110011</td><td align = "center">3</td></tr>
       <tr><td align = "center">52</td><td align = "center">064</td><td align = "center">34</td><td align = "center">00110100</td><td align = "center">4</td></tr>
       <tr><td align = "center">53</td><td align = "center">065</td><td align = "center">35</td><td align = "center">00110101</td><td align = "center">5</td></tr>
       <tr><td align = "center">54</td><td align = "center">066</td><td align = "center">36</td><td align = "center">00110110</td><td align = "center">6</td></tr>
       <tr><td align = "center">55</td><td align = "center">067</td><td align = "center">37</td><td align = "center">00110111</td><td align = "center">7</td></tr>
       <tr><td align = "center">56</td><td align = "center">070</td><td align = "center">38</td><td align = "center">00111000</td><td align = "center">8</td></tr>
       <tr><td align = "center">57</td><td align = "center">071</td><td align = "center">39</td><td align = "center">00111001</td><td align = "center">9</td></tr>
       <tr><td align = "center">58</td><td align = "center">072</td><td align = "center">3A</td><td align = "center">00111010</td><td align = "center">:</td></tr>
       <tr><td align = "center">59</td><td align = "center">073</td><td align = "center">3B</td><td align = "center">00111011</td><td align = "center">;</td></tr>
       <tr><td align = "center">60</td><td align = "center">074</td><td align = "center">3C</td><td align = "center">00111100</td><td align = "center">&lt;</td></tr>
       <tr><td align = "center">61</td><td align = "center">075</td><td align = "center">3D</td><td align = "center">00111101</td><td align = "center">=</td></tr>
       <tr><td align = "center">62</td><td align = "center">076</td><td align = "center">3E</td><td align = "center">00111110</td><td align = "center">&gt;</td></tr>
       <tr><td align = "center">63</td><td align = "center">077</td><td align = "center">3F</td><td align = "center">00111111</td><td align = "center">?</td></tr>
       <tr><td align = "center">64</td><td align = "center">100</td><td align = "center">40</td><td align = "center">01000000</td><td align = "center">@</td></tr>
       <tr><td align = "center">65</td><td align = "center">101</td><td align = "center">41</td><td align = "center">01000001</td><td align = "center">A</td></tr>
       <tr><td align = "center">66</td><td align = "center">102</td><td align = "center">42</td><td align = "center">01000010</td><td align = "center">B</td></tr>
       <tr><td align = "center">67</td><td align = "center">103</td><td align = "center">43</td><td align = "center">01000011</td><td align = "center">C</td></tr>
       <tr><td align = "center">68</td><td align = "center">104</td><td align = "center">44</td><td align = "center">01000100</td><td align = "center">D</td></tr>
       <tr><td align = "center">69</td><td align = "center">105</td><td align = "center">45</td><td align = "center">01000101</td><td align = "center">E</td></tr>
       <tr><td align = "center">70</td><td align = "center">106</td><td align = "center">46</td><td align = "center">01000110</td><td align = "center">F</td></tr>
       <tr><td align = "center">71</td><td align = "center">107</td><td align = "center">47</td><td align = "center">01000111</td><td align = "center">G</td></tr>
       <tr><td align = "center">72</td><td align = "center">110</td><td align = "center">48</td><td align = "center">01001000</td><td align = "center">H</td></tr>
       <tr><td align = "center">73</td><td align = "center">111</td><td align = "center">49</td><td align = "center">01001001</td><td align = "center">I</td></tr>
       <tr><td align = "center">74</td><td align = "center">112</td><td align = "center">4A</td><td align = "center">01001010</td><td align = "center">J</td></tr>
       <tr><td align = "center">75</td><td align = "center">113</td><td align = "center">4B</td><td align = "center">01001011</td><td align = "center">K</td></tr>
       <tr><td align = "center">76</td><td align = "center">114</td><td align = "center">4C</td><td align = "center">01001100</td><td align = "center">L</td></tr>
       <tr><td align = "center">77</td><td align = "center">115</td><td align = "center">4D</td><td align = "center">01001101</td><td align = "center">M</td></tr>
       <tr><td align = "center">78</td><td align = "center">116</td><td align = "center">4E</td><td align = "center">01001110</td><td align = "center">N</td></tr>
       <tr><td align = "center">79</td><td align = "center">117</td><td align = "center">4F</td><td align = "center">01001111</td><td align = "center">O</td></tr>
       <tr><td align = "center">80</td><td align = "center">120</td><td align = "center">50</td><td align = "center">01010000</td><td align = "center">P</td></tr>
       <tr><td align = "center">81</td><td align = "center">121</td><td align = "center">51</td><td align = "center">01010001</td><td align = "center">Q</td></tr>
       <tr><td align = "center">82</td><td align = "center">122</td><td align = "center">52</td><td align = "center">01010010</td><td align = "center">R</td></tr>
       <tr><td align = "center">83</td><td align = "center">123</td><td align = "center">53</td><td align = "center">01010011</td><td align = "center">S</td></tr>
       <tr><td align = "center">84</td><td align = "center">124</td><td align = "center">54</td><td align = "center">01010100</td><td align = "center">T</td></tr>
       <tr><td align = "center">85</td><td align = "center">125</td><td align = "center">55</td><td align = "center">01010101</td><td align = "center">U</td></tr>
       <tr><td align = "center">86</td><td align = "center">126</td><td align = "center">56</td><td align = "center">01010110</td><td align = "center">V</td></tr>
       <tr><td align = "center">87</td><td align = "center">127</td><td align = "center">57</td><td align = "center">01010111</td><td align = "center">W</td></tr>
       <tr><td align = "center">88</td><td align = "center">130</td><td align = "center">58</td><td align = "center">01011000</td><td align = "center">X</td></tr>
       <tr><td align = "center">89</td><td align = "center">131</td><td align = "center">59</td><td align = "center">01011001</td><td align = "center">Y</td></tr>
       <tr><td align = "center">90</td><td align = "center">132</td><td align = "center">5A</td><td align = "center">01011010</td><td align = "center">Z</td></tr>
       <tr><td align = "center">91</td><td align = "center">133</td><td align = "center">5B</td><td align = "center">01011011</td><td align = "center">[</td></tr>
       <tr><td align = "center">92</td><td align = "center">134</td><td align = "center">5C</td><td align = "center">01011100</td><td align = "center">\</td></tr>
       <tr><td align = "center">93</td><td align = "center">135</td><td align = "center">5D</td><td align = "center">01011101</td><td align = "center">]</td></tr>
       <tr><td align = "center">94</td><td align = "center">136</td><td align = "center">5E</td><td align = "center">01011110</td><td align = "center">^</td></tr>
       <tr><td align = "center">95</td><td align = "center">137</td><td align = "center">5F</td><td align = "center">01011111</td><td align = "center">_</td></tr>
       <tr><td align = "center">96</td><td align = "center">140</td><td align = "center">60</td><td align = "center">01100000</td><td align = "center">`</td></tr>
       <tr><td align = "center">97</td><td align = "center">141</td><td align = "center">61</td><td align = "center">01100001</td><td align = "center">a</td></tr>
       <tr><td align = "center">98</td><td align = "center">142</td><td align = "center">62</td><td align = "center">01100010</td><td align = "center">b</td></tr>
       <tr><td align = "center">99</td><td align = "center">143</td><td align = "center">63</td><td align = "center">01100011</td><td align = "center">c</td></tr>
       <tr><td align = "center">100</td><td align = "center">144</td><td align = "center">64</td><td align = "center">01100100</td><td align = "center">d</td></tr>
       <tr><td align = "center">101</td><td align = "center">145</td><td align = "center">65</td><td align = "center">01100101</td><td align = "center">e</td></tr>
       <tr><td align = "center">102</td><td align = "center">146</td><td align = "center">66</td><td align = "center">01100110</td><td align = "center">f</td></tr>
       <tr><td align = "center">103</td><td align = "center">147</td><td align = "center">67</td><td align = "center">01100111</td><td align = "center">g</td></tr>
       <tr><td align = "center">104</td><td align = "center">150</td><td align = "center">68</td><td align = "center">01101000</td><td align = "center">h</td></tr>
       <tr><td align = "center">105</td><td align = "center">151</td><td align = "center">69</td><td align = "center">01101001</td><td align = "center">i</td></tr>
       <tr><td align = "center">106</td><td align = "center">152</td><td align = "center">6A</td><td align = "center">01101010</td><td align = "center">j</td></tr>
       <tr><td align = "center">107</td><td align = "center">153</td><td align = "center">6B</td><td align = "center">01101011</td><td align = "center">k</td></tr>
       <tr><td align = "center">108</td><td align = "center">154</td><td align = "center">6C</td><td align = "center">01101100</td><td align = "center">l</td></tr>
       <tr><td align = "center">109</td><td align = "center">155</td><td align = "center">6D</td><td align = "center">01101101</td><td align = "center">m</td></tr>
       <tr><td align = "center">110</td><td align = "center">156</td><td align = "center">6E</td><td align = "center">01101110</td><td align = "center">n</td></tr>
       <tr><td align = "center">111</td><td align = "center">157</td><td align = "center">6F</td><td align = "center">01101111</td><td align = "center">o</td></tr>
       <tr><td align = "center">112</td><td align = "center">160</td><td align = "center">70</td><td align = "center">01110000</td><td align = "center">p</td></tr>
       <tr><td align = "center">113</td><td align = "center">161</td><td align = "center">71</td><td align = "center">01110001</td><td align = "center">q</td></tr>
       <tr><td align = "center">114</td><td align = "center">162</td><td align = "center">72</td><td align = "center">01110010</td><td align = "center">r</td></tr>
       <tr><td align = "center">115</td><td align = "center">163</td><td align = "center">73</td><td align = "center">01110011</td><td align = "center">s</td></tr>
       <tr><td align = "center">116</td><td align = "center">164</td><td align = "center">74</td><td align = "center">01110100</td><td align = "center">t</td></tr>
       <tr><td align = "center">117</td><td align = "center">165</td><td align = "center">75</td><td align = "center">01110101</td><td align = "center">u</td></tr>
       <tr><td align = "center">118</td><td align = "center">166</td><td align = "center">76</td><td align = "center">01110110</td><td align = "center">v</td></tr>
       <tr><td align = "center">119</td><td align = "center">167</td><td align = "center">77</td><td align = "center">01110111</td><td align = "center">w</td></tr>
       <tr><td align = "center">120</td><td align = "center">170</td><td align = "center">78</td><td align = "center">01111000</td><td align = "center">x</td></tr>
       <tr><td align = "center">121</td><td align = "center">171</td><td align = "center">79</td><td align = "center">01111001</td><td align = "center">y</td></tr>
       <tr><td align = "center">122</td><td align = "center">172</td><td align = "center">7A</td><td align = "center">01111010</td><td align = "center">z</td></tr>
       <tr><td align = "center">123</td><td align = "center">173</td><td align = "center">7B</td><td align = "center">01111011</td><td align = "center">{</td></tr>
       <tr><td align = "center">124</td><td align = "center">174</td><td align = "center">7C</td><td align = "center">01111100</td><td align = "center">|</td></tr>
       <tr><td align = "center">125</td><td align = "center">175</td><td align = "center">7D</td><td align = "center">01111101</td><td align = "center">}</td></tr>
       <tr><td align = "center">126</td><td align = "center">176</td><td align = "center">7E</td><td align = "center">01111110</td><td align = "center">~</td></tr>
       <tr><td align = "center">127</td><td align = "center">177</td><td align = "center">7F</td><td align = "center">01111111</td><td align = "center">DEL</td></tr>
            </tbody>

        </table>

""")
        self.edit.moveCursor(QTextCursor.Start)
        self.setWidget(self.edit)