# Programm zur Simulation einer gehebelten Rotations-Strategie
Inspiriert von dem wissenschaftlichen Paper "Leverage for the Long Run - A Systematic Approach to Managing Risk and Magnifying Returns in Stocks" von M. Gayed.

Die Simulation berechnet dabei Gebühren wie TER, Spreads, Kapitalertragssteuer, Solidaritätszuschlag und (sofern eingestellt) Wikifolio Gebühren mit ein.
Zudem geht die Simulation davon aus, dass am Ende des Simulationszeitraum die Gewinne realisiert werden und damit Steuern auf Diese anfallen.
Als Fenstergröße wurde diejenige bestimmt, die das größte Gesamtwachtum des Kapitals bewirkt hätte. Dabei wurden alle Fenstergrößen von 10 bis 300 ausprobiert in Zehner-Schritten.

Für Buy And Hold wird ein Spread von 0.0002 angenommen.
Für die Rotationsstrategie wird aufgrund der geringeren Liquidität der Hebel-ETFs ein Spread von 0.0015% p.a. angenommen. Die Spreads können schwanken, dürften aber nahe an der Realität sein.
Die Parameter der Wikifolio Simulation wurden auf 0.95% p.a. Zertifikatsgebühr und 5% Performancegebühr gesetzt.
Der Simulationszeitraum ist der 18.01.1994 bis 18.01.2024, wobei die ersten x-Tage nur für die SMA Berechnung und verwendet werden, um danach die Strategie durchzuführen (z.B. x=200 Tage oder x=260 Tage).
Dividenten sind nicht miteinberechnet, da die ich keine (kommerziell nutzbaren) Daten dazu habe. Die tatsächlichen historischen Renditen dürften entsprechend noch etwas höher sein.
Eine Rotation in Staatsanleihen, wie in dem Paper beschrieben wird ebenfalls nicht simuliert.

Die Strategien kann man selbst manuell mit einem Broker durchführen. Dazu müsste man jeden Tag die Gleitenden Durchschnitte berechnen und je nachdem ob der ungebelte Kurs des Indizes darüber liegt kaufen bzw. ansonsten verkaufen. Für wen das zu viel Aufwand ist, hab ich auch passende Wikifolios erstellt, die die entsprechend der Simulation historisch besten Parameter verwenden, zu finden hier:

https://www.wikifolio.com/de/de/p/lstrategies?tab=wikifolios.

## S&P 500
### Parameter für den S&P 500
TER Buy and Hold: 0.07%

TER 2x ETF: 0.6%

TER 3x ETF: 0.75%

### Ergebnisse auf S&P 500 mit 200 Tage SMA (wie im Paper)
| Strategy                   | Total Growth    | CAGR  | Max Drawdown  |
| -------------------------- | --------- | ----- | ------------- |
| Buy and Hold               | x7.62     | 7.2%  | -56.82%       |
| Rotary Broker 2x           | x13.17    | 9.22% | -54.1%        |
| Rotary Wikifolio 2x        | x9.56     | 8.03% | -54.91%       |
| Rotary Broker 3x           | x34.38    | 12.87%| -69.81%       |
| Rotary Wikifolio 3x        | x23.0     | 11.32%| -70.42%       |


### Ergebnisse auf S&P 500 mit 260 Tage SMA (Beste Fenstergröße)
| Strategy                | Total Growth   | CAGR   | Max Drawdown   |
|-------------------------|----------|--------|----------------|
| Buy and Hold            | x7.59    | 7.24%  | -56.82%        |
| Rotary Broker 2x        | x26.01   | 11.9%  | -48.62%        |
| Rotary Wikifolio 2x     | x18.1    | 10.51% | -36.53%        |
| Rotary Broker 3x        | x89.92   | 16.79% | -60.56%        |
| Rotary Wikifolio 3x     | x55.31   | 14.85% | -51.59%        |


## NASDAQ 100
### Parameter für den NASDAQ 100
TER Buy and Hold: 0.2%

TER 2x ETF: 0.6%

TER 3x ETF: 0.75%

### Ergebnisse auf NASDAQ 100 mit 200 Tage SMA (wie im Paper)
| Strategy                   | Total Growth   | CAGR    | Max Drawdown |
| -------------------------- | -------- | ------- | ------------ |
| Buy and Hold               | x29.02   | 12.21%  | -82.98%      |
| Rotary Broker 2x           | x113.18  | 17.56%  | -88.41%      |
| Rotary Wikifolio 2x        | x69.91   | 15.64%  | -86.06%      |
| Rotary Broker 3x           | x334.02  | 21.99%  | -96.37%      |
| Rotary Wikifolio 3x        | x171.54  | 19.25%  | -95.59%      |


### Ergebnisse auf NASDAQ 100 mit 240 Tage SMA (Beste Fenstergröße)
| Strategy                    | Total Growth    | CAGR   | Max Drawdown   |
|-----------------------------|-----------|--------|----------------|
| Buy and Hold                | x29.36    | 12.33% | -82.98%        |
| Rotary Broker 2x            | x316.62   | 21.9%  | -79.18%        |
| Rotary Wikifolio 2x         | x253.79   | 20.98% | -74.9%         |
| Rotary Broker 3x            | x1522.1   | 28.67% | -91.49%        |
| Rotary Wikifolio 3x         | x1073.44  | 27.13% | -89.64%        |
