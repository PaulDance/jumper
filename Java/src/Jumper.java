import java.awt.Color;
import java.util.ArrayList;
import processing.core.PApplet;
import processing.core.PShape;

import java.io.*;

public class Jumper extends PApplet {

	private int paddlesWidth = 120, paddlesHeight = 18, winWidth = 500, winHeight = 800, BlueSize = 40, scoreUp = 0, scoreUpMax, textState = 0, t0 = millis();		// Settings
	private float gravityAcceleration = (float) 1.25, horizontalAcceleration = (float) 0.75, maxHorzSpeed = 7, maxVertSpeed = 12, jumpSpeed = 20;
	private static int highScore = 0;
	private boolean onGround = true, running = false;
	Blue Blue;
	Paddles paddles;
	
	
	public static void main(String[] args) {
		
		try {
			FileReader fr = new FileReader(".HighScore.dat");		// We try to open the highscore file, to get the last highscore.
			BufferedReader br = new BufferedReader(fr);
			int charCode, charCount = -1;
			
			while ((charCode = br.read()) != -1) {					// Counting how many characters are in the file.
				charCount++;
			}
			
			fr = new FileReader(".HighScore.dat");					// Reseting the file reader, to start at the beginning again.
			br = new BufferedReader(fr);
			
			while ((charCode = br.read()) != -1) {
				highScore += pow(10, charCount) * (charCode - 48);	// Parsing the number into a variable.
				charCount--;
			}
			
			br.close();												// Close the file reader for things to take effect.
		}
		catch (IOException e) {										// If the file does not exist,
			try {
				FileWriter fw = new FileWriter(".HighScore.dat");	// make a new one,
				PrintWriter pw = new PrintWriter(fw);
				
				pw.print("0");										// and write a score of zero in it.
				pw.close();											// Close the file writer for things to take effect.
			}
			catch (IOException ex) {
				System.out.println("An error occuried while trying to open '.HighScore.dat'");
			}
		}
		
		PApplet.main("Jumper");										// Start the Processing Applet.
	}
	
	
	public void settings() {
		size(winWidth, winHeight);		// Window size settings.
		pixelDensity(displayDensity());	// To adapt display to current screen.
		smooth(4);						// Smooth : anti-aliasing setting (here : 4x).
	}
	
	public void setup() {
		ellipseMode(CENTER);			// Coordinates focus on center of shapes.
		rectMode(CENTER);
		shapeMode(CENTER);
		strokeJoin(ROUND);
		textAlign(CENTER, CENTER);
		background(255);				// Background color in gray scale (black here).
		frameRate(60);
		Blue = new Blue(winWidth / 2, winHeight - 50 - (BlueSize/2) - (paddlesHeight/2), 0, jumpSpeed, BlueSize, Color.BLUE);
		paddles = new Paddles(Color.RED);
		gameStartText();
	}
	
	public void draw() {							// Core looping method.
		if (textState == -1) {
			if (focused) {							// We detect if the window has the focus (== is active), else make a pause screen.
				//fpsDisplay(10);
				
				fill(255);								// Color of shapes filling.
				rect(width / 2, height / 2, width - 1, height - 1);		// Erase everything.
				strokeWeight(0);
				Blue.paint();		// Paint : graphic update
				Blue.update();		// Update : data update
				paddles.paint();
				paddles.update();
				
				
				if (scoreUp == scoreUpMax + 1) {		// To fix a weird bug that happened while bouncing on place,
					scoreUp -= 1;						// where the scoreUpMax would slowly go up one by one approximately every second.
				}
				
				if (scoreUp / 10 > scoreUpMax) {		// scoreUpMax is the best score that has been obtained in the same round,
					scoreUpMax = scoreUp / 10;			// so that the display doesn't go up and down all the time.
				}
				
				if (scoreUpMax > highScore) {			// HighScore condition.
					highScore = scoreUpMax;
				}
				
				fill(230, 210, 20);
				stroke(255, 255, 0);		// Text settings.
				strokeWeight(2);
				textSize(20);
				
				textAlign(CORNER, CENTER);
				text("Score : " + str(scoreUpMax), 30, 30);		// Refresh scores text.
				text("HighScore : " + str(highScore), width - 200, 30);
				textAlign(CENTER, CENTER);
				
				if (Blue.y > height + BlueSize) {		// Game over condition.
					running = false;
					strokeWeight(0);
					fill(255);
					rect(width / 2, height / 2, width, height);
					
					textState = 2;
					gameOverText();
				}
			}
			else {				// We make here the pause screen with a pause logo and an animation.
				fill(255, 255, 255, 20);
				strokeWeight(0);
				rect(width / 2, height / 2, width, height);
				
				fill(Color.CYAN.getRGB());
				stroke(0, 0, 255);
				strokeWeight(2);
				rect(width / 2 - 50, height / 2, 50, 150);
				rect(width / 2 + 50, height / 2, 50, 150);
			}
		}
		else if (textState <= 1)
			gameStartText();
		else if (textState <= 4)
			gameOverText();
	}
	
	private void fpsDisplay(double frequency) {
		if ((millis() - t0) / 1000.0 >= 1.0 / frequency) {
			frameCount = 0;
			t0 = millis();
			
			if (20 <= frameRate && frameRate < 59)
				println(frameRate);
		}
	}
	
	
	private class Blue {				// Ball class
		
		float x, y, maxY, vx, vy, size;	// x : x position, y : y position, vx : speed on x axis, vy speed on y axis, size : radius.
		Color color;					// Java color object.
		PShape renderedShape;
		
		private Blue(float nx, float ny, float nvx, float nvy, float nsize, Color c) {		// Constructor
			
			x = nx;
			maxY = y = ny;
			vx = nvx;
			vy = nvy;
			size = nsize;				// Initialization of above the attributes.
			color = c;
			
			renderedShape = createShape(ELLIPSE, 0, 0, nsize, nsize);
			renderedShape.setName("Blue");
			renderedShape.setFill(color(color.getRed(), color.getGreen(), color.getBlue()));
			renderedShape.setStroke(color(Color.CYAN.getRed(), Color.CYAN.getGreen(), Color.CYAN.getBlue()));
			renderedShape.setStrokeWeight(1);
			
		}
		
		private void paint() {			// Paint Blue again.
			shape(renderedShape, x, y);
		}
		
		private void update() {
			x += vx;
			
			if (keyPressed) {
				if (keyCode == LEFT && running && (abs(vx) <= maxHorzSpeed || vx >= maxHorzSpeed)) {			// Left movement.
					vx -= horizontalAcceleration;
				}
				else if (keyCode == RIGHT && running && (abs(vx) <= maxHorzSpeed || vx <= -maxHorzSpeed)) {		// Right movement
					vx += horizontalAcceleration;
				}
				else if (key == ' ' && !running) {		// Beginning of the game using space.
					running = true;						// Running will be used to stop the game at will (without using exit()).
					onGround = false;					// onGround is used to stop vertical movement when needed, see below.
					vy = jumpSpeed;						// vy is the vertical speed, see below.
				}
			}
			
			if (x < 0)
				x += width;
			
			else if (x > width)
				x -= width;
			
			if (running && !onGround) {					// Here's the use of onGround : stop vertical movement if Blue is above the third of the window.
				y -= vy;
				
				if (vy >= -maxVertSpeed)
					vy -= gravityAcceleration;
				
				if (vy >= 0 && maxY > y)
					maxY = y;
			}
			else if (running && onGround) {				// In the case Blue is above the third of the window, scroll down the paddles, using a vy.
				for (int i = 0; i < paddles.paddlesList.size(); i++)
					paddles.paddlesList.get(i).y += vy;
				
				scoreUp += vy;
				
				if (vy > -maxVertSpeed)
					vy -= gravityAcceleration;
			}
		}
	}
	
	
	private class Paddles {		// The paddles class.
		
		ArrayList<Paddle> paddlesList = new ArrayList<Paddle>();	// An ArrayList that will contain every paddle.
		float wid = paddlesWidth, hei = paddlesHeight;				// Width and height.
		Color color;												// Again, a color.
		PShape renderedShape;
		
		private Paddles(Color c) {
			
				paddlesList.add(new Paddle(width / 2, height - 50, paddlesWidth, paddlesHeight));		// Initialization : add the beginning paddle.
				color = c;
				renderedShape = createShape(RECT, 0, 0, paddlesWidth, paddlesHeight);
				renderedShape.setFill(color(color.getRed(), color.getGreen(), color.getBlue()));
				renderedShape.setStrokeWeight(1);
				renderedShape.setStroke(0);
				
		}
		
		private void update() {
			for (int i = 0; i < paddlesList.size(); i++) {
				if (Blue.vy <= 0 && Blue.maxY + Blue.size/2 - 5 <= paddlesList.get(i).y - hei) {
					if (paddlesList.get(i).y - hei <= Blue.y + Blue.size/2 - 5 && Blue.y + Blue.size/2 - 5 <= paddlesList.get(i).y + hei && paddlesList.get(i).x - wid/2 <= Blue.x && Blue.x <= paddlesList.get(i).x + wid/2) {		// Ball and paddle collision detection
						Blue.vy = jumpSpeed;		// If touched : bounce, so go up.
						Blue.maxY = Blue.y;
					}
				}
				else if (paddlesList.get(i).y > height + paddlesList.get(i).hei/2) {
					paddlesList.remove(i);				// Otherwise, if the paddle is below the bottom side of the window, delete it.
				}
			}
			
			while (paddlesList.get(paddlesList.size()-1).y > 20) {		// New paddle generation while the last one has a y position > 20 pixels.
				float a = random(-width, width);						// a is the random x variation, relatively to the last paddle.
				
				while (paddlesList.get(paddlesList.size()-1).x + a > width - paddlesWidth / 2 || paddlesList.get(paddlesList.size()-1).x + a < paddlesWidth / 2) {		// We use a while loop to make sure it doesn't go outside the window.
					a = random(-width, width);
				}
				
				paddlesList.add(new Paddle(paddlesList.get(paddlesList.size()-1).x + a, paddlesList.get(paddlesList.size()-1).y - random(60, 120), paddlesWidth, paddlesHeight));		// Then add the new random paddle.
			}
			
			if (Blue.y < 2 * height / 3 && running && !onGround) {		// If Blue is above the third of the window, stop it and scroll down the paddlesList until moveModeTemp == 0 (see above).
				onGround = true;
			}
			else if (Blue.vy <= 0) {
				onGround = false;
			}
		}
		
		private void paint() {
			for (int i = 0; i < paddlesList.size(); i++) {
				shape(renderedShape, paddlesList.get(i).x, paddlesList.get(i).y);		// Make a rectangle on every paddle position.
			}
		}
	
	
		private class Paddle {		// Just a very small class to create paddle objects and to store them in an ArrayList.
			
			float x, y, wid, hei;
			
			private Paddle(float px, float py, float w, float h) {
				
				x = px;
				y = py;
				wid = w;			// Initialization of the above attributes.
				hei = h;
				
			}
		}
	}
	
	private void waitListen(int time) {
		int clock = 0;
		
		while (!keyPressed && key != ' ' && clock < time) {
			delay((int)(1000f / frameRate));
			clock += (int)(1000f / frameRate);
		}
	}
	
	private void gameStartText() {
		if (textState == 0) {
			fill(70, 70, 255);
			stroke(30, 30, 255);
			strokeWeight(2);
			textSize(60);
			text("Press Space to\nStart !", width / 2, height / 2);
			textState += 1;
		}
		else if (textState == 1) {
			delay(2000);
			//waitListen(2000);
			textState = -1;
		}
	}
	
	private void gameOverText() {
		if (textState == 2) {
			delay(500);
			
			fill(255, 70, 70);
			stroke(255, 30, 30);
			strokeWeight(2);
			textSize(70);
			
			text("Game Over !\nYou Lose !", width / 2, height / 2);
			textState += 1;
		}
		else if (textState == 3) {
			delay(2000);
			//waitListen(2000);
			
			background(255);
			fill(70, 255, 70);
			stroke(30, 255, 30);
			strokeWeight(2);
			
			if (scoreUpMax == highScore) {
				text("You beat the\nhigh score !", width / 2, height / 3);
				text("It is now :\n" + str(highScore), width / 2, 2 * height / 3);
				
				try {
					FileWriter fw = new FileWriter(".HighScore.dat");
					PrintWriter pw = new PrintWriter(fw);
					
					pw.print(str(highScore));			// We write the new highscore.
					pw.close();
				}
				catch (IOException ex) {
					System.out.println("An error occuried while trying to write to '.HighScore.dat'");
				}
			}
			else {
				text("Your score is :\n" + str(scoreUpMax), width / 2, height / 2);
			}
			textState += 1;
		}
		else if (textState == 4) {
			delay(3000);
			//waitListen(3000);
			background(255);
			
			scoreUp = 0;		// Restart at game end (the program is then endless).
			scoreUpMax = 0;
			Blue = new Blue(winWidth / 2, winHeight - 50 - (BlueSize/2) - (paddlesHeight/2), 0, jumpSpeed, BlueSize, Color.BLUE);
			paddles = new Paddles(Color.RED);
			textState = 0;
		}
	}
}
