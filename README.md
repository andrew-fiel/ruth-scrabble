# Ruth-Scrabble
This project is being built with the intention of eventually running on an Arduino-run physical Scrabble board. "Ruth" is my grandma, who plays a lot of Scrabble, but does not often have opponents to play against.

## Sources That Helped
- Scrabble algorithm based on [this paper](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf).
- DAWG implementation based on [this](https://gist.github.com/smhanov/94230b422c2100ae4218).
## Heatmap
This heatmap represents the locations of tiles from the highest scoring words in 1000 games played with one rack. On average, the games took 1.614 seconds each.
![1000bettergames](https://user-images.githubusercontent.com/43427035/69286614-f1f90580-0bb0-11ea-90cf-3eb3ce8e9ce3.png)

The following variation explicitly marks special-value tiles.

DL = Double Letter Score

TL = Triple Letter Score

DW = Double Word Score

TW = Triple Word Score

![1000bettergamesedit](https://user-images.githubusercontent.com/43427035/69286650-063d0280-0bb1-11ea-9c0a-8c72299c96ac.png)
