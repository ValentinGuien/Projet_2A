#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <math.h>
#include <Adafruit_PWMServoDriver.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

/*--------------------------------------setup------------------------------------*/

int pinBouton = 13;
int pinAdrPlateau0 = 2;
int pinAdrPlateau1 = 3;
int pinAdrPlateau2 = 4;
int pinAdrPlateau3 = 5;
int pinAdrPlateau4 = 6;
int pinAdrPlateau5 = 7;
int pinEnablePlateau = 10;
int plateau[8][8] = {{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0}};
int pinAimant = 12;
double angleBase = 90;
double angleEpaule = 110;
double angleCoude = 40;
double anglePoignet = 90 ;
Adafruit_PWMServoDriver pca= Adafruit_PWMServoDriver(0x41);
int servoBase = 15;
int servoEpaule = 11;
int servoCoude = 7;
int servoPoignet = 3;
double correctifBase = 14.5;
double correctifEpaule = -15;
double correctifCoude = 0;
double correctifPoignet = -100;

void setup() {
  
  //initialisation de l'afficheur
  lcd.init();
  lcd.backlight();

  //initialisation du bouton
  pinMode(pinBouton, INPUT);

  //initialisation plateau
  pinMode(pinAdrPlateau0, OUTPUT);
  pinMode(pinAdrPlateau1, OUTPUT);
  pinMode(pinAdrPlateau2, OUTPUT);
  pinMode(pinAdrPlateau3, OUTPUT);
  pinMode(pinAdrPlateau4, OUTPUT);
  pinMode(pinAdrPlateau5, OUTPUT);
  pinMode(pinEnablePlateau, OUTPUT);
  pinMode(A0, INPUT); //sortie plateau
  digitalWrite(pinAdrPlateau0, LOW);
  digitalWrite(pinAdrPlateau1, LOW);
  digitalWrite(pinAdrPlateau2, LOW);
  digitalWrite(pinAdrPlateau3, LOW);
  digitalWrite(pinAdrPlateau4, LOW);
  digitalWrite(pinAdrPlateau5, LOW);
  digitalWrite(pinEnablePlateau, LOW);

  //initialisation de l'aimant
  pinMode(pinAimant, OUTPUT);
  digitalWrite(pinAimant, LOW);

  //initialisation du bras
  pca.begin();
  pca.setPWMFreq(50);
  delay(100);
  bouger_servo(servoBase, angleBase);
  bouger_servo(servoEpaule, angleEpaule);
  bouger_servo(servoCoude, angleCoude);
  bouger_servo(servoPoignet, anglePoignet);
}

/*--------------------------------------loop-------------------------------------*/

void loop() {
  if(etat_bouton() == true){
    bouger_bras(20, 4, 20, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    bouger_bras(20, 0, 20, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    activer_aimant();
    bouger_bras(20, 4, 20, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    bouger_bras(29.3, 4, -11, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    bouger_bras(29.3, 1, -11, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    desactiver_aimant();
    bouger_bras(29.3, 4, -11, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    bouger_bras(20, 10, 0, &angleBase, &angleEpaule, &angleCoude, &anglePoignet);
    //etat_plateau(plateau);
    //afficher_plateau(plateau);
  }
}

/*-----------------------------------Mes fonctions---------------------------------*/

void afficher_lcd(String ligne1, String ligne2, String ligne3, String ligne4){   //l'écran lcd a 4 lignes et 20 colonnes
    lcd.setCursor(0,0);
    lcd.print(ligne1.substring(0,20));
    lcd.setCursor(0,1);
    lcd.print(ligne2.substring(0,20));
    lcd.setCursor(0,2);
    lcd.print(ligne3.substring(0,20));
    lcd.setCursor(0,3);
    lcd.print(ligne4.substring(0,20));
}

bool etat_bouton(){
  return((digitalRead(pinBouton)==HIGH)?true:false);
}

bool etat_case(int adresseDecimal){
  int temp = adresseDecimal;
  int adresse[6] = {0, 0, 0, 0, 0, 0};
  for (int i=5;i>=0;i--){   // itère pour 6 bits
    adresse[i]=temp & 1;  // prend le LSB et le sauve dans adresse
    temp = temp >> 1;    // décalage d'un bit sur la droite
  }
  Serial.println(String(adresse[0]) + String(adresse[1]) + String(adresse[2]) + String(adresse[3]) + String(adresse[4]) + String(adresse[5]));
  digitalWrite(pinAdrPlateau0, (adresse[5]==0?LOW:HIGH));
  digitalWrite(pinAdrPlateau1, (adresse[4]==0?LOW:HIGH));
  digitalWrite(pinAdrPlateau2, (adresse[3]==0?LOW:HIGH));
  digitalWrite(pinAdrPlateau3, (adresse[2]==0?LOW:HIGH));
  digitalWrite(pinAdrPlateau4, (adresse[1]==0?LOW:HIGH));
  digitalWrite(pinAdrPlateau5, (adresse[0]==0?LOW:HIGH));
  delay(10);
  return (analogRead(A0)>100?true:false);
}

void etat_plateau(int plateau[8][8]){
  digitalWrite(pinEnablePlateau, HIGH); //on active le plateau
  for(int ligne = 0; ligne < 8; ligne ++){
    for(int colonne = 0; colonne < 8; colonne ++){
      plateau[ligne][colonne] = etat_case(ligne * 8 + colonne);
    }
  }
  digitalWrite(pinEnablePlateau, LOW); //on désactive le plateau
}

void afficher_plateau(int plateau[8][8]){
  afficher_lcd("|" + String(plateau[0][0]) + String(plateau[0][1]) + String(plateau[0][2]) + String(plateau[0][3]) + String(plateau[0][4]) + String(plateau[0][5]) + String(plateau[0][6]) + String(plateau[0][7]) + "||" + String(plateau[4][0]) + String(plateau[4][1]) + String(plateau[4][2]) + String(plateau[4][3]) + String(plateau[4][4]) + String(plateau[4][5]) + String(plateau[4][6]) + String(plateau[4][7]) + "|",
               "|" + String(plateau[1][0]) + String(plateau[1][1]) + String(plateau[1][2]) + String(plateau[1][3]) + String(plateau[1][4]) + String(plateau[1][5]) + String(plateau[1][6]) + String(plateau[1][7]) + "||" + String(plateau[5][0]) + String(plateau[5][1]) + String(plateau[5][2]) + String(plateau[5][3]) + String(plateau[5][4]) + String(plateau[5][5]) + String(plateau[5][6]) + String(plateau[5][7]) + "|",
               "|" + String(plateau[2][0]) + String(plateau[2][1]) + String(plateau[2][2]) + String(plateau[2][3]) + String(plateau[2][4]) + String(plateau[2][5]) + String(plateau[2][6]) + String(plateau[2][7]) + "||" + String(plateau[6][0]) + String(plateau[6][1]) + String(plateau[6][2]) + String(plateau[6][3]) + String(plateau[6][4]) + String(plateau[6][5]) + String(plateau[6][6]) + String(plateau[6][7]) + "|",
               "|" + String(plateau[3][0]) + String(plateau[3][1]) + String(plateau[3][2]) + String(plateau[3][3]) + String(plateau[3][4]) + String(plateau[3][5]) + String(plateau[3][6]) + String(plateau[3][7]) + "||" + String(plateau[7][0]) + String(plateau[7][1]) + String(plateau[7][2]) + String(plateau[7][3]) + String(plateau[7][4]) + String(plateau[7][5]) + String(plateau[7][6]) + String(plateau[7][7]) + "|");
}

void activer_aimant(){
  delay(100);
  digitalWrite(pinAimant, HIGH);
  delay(500);
}

void desactiver_aimant(){
  delay(100);
  digitalWrite(pinAimant, LOW);
  delay(500);
}

void calcul_angles_bras(double xp, double yp, double zp, double * angleBase, double * angleEpaule, double * angleCoude, double * anglePoignet){ //xp, yp et zp sont les coordonnées du point à atteindre en cm
  //longueurs des différents segments du bras en cm:
  yp = yp -1; //correctif
  double d0 = 3.8;
  double d1 = 23.45;
  double d2 = 29.95;
  double d3 = 5.5;
  //variables temporaires 
  double xa = 0;
  double ya = d0;
  double xb = xp;
  double yb = yp + d3;
  double a = 2*(xb-xa);
  double b = 2*(yb-ya);
  double r = d1;
  double R = d2;
  double c = pow((xb - xa),2) + pow((yb - ya),2) - pow(R,2) + pow(r,2);
  double delta = pow((2*a*c),2) - 4 * (pow(a,2) + pow(b,2))* (pow(c,2) - pow(b,2) * pow(r,2));
  double x1 = xa + (2*a*c-sqrt(delta))/(2*(pow(a,2)+pow(b,2)));
  double x2 = xa + (2*a*c+sqrt(delta))/(2*(pow(a,2)+pow(b,2)));
  double y1 = 0;
  double y2 = 0;
  double xc = 0;
  double yc = 0;
  if(b != 0){
    y1 = ya + (c - a*(x1 - xa))/b;
    y2 = ya + (c - a*(x2 - xa))/b;
  }
  else{
    y1 = ya + b/2 + sqrt(pow(R,2) - pow(((2*c-pow(a,2))/(2*a)),2));
    y2 = ya + b/2 - sqrt(pow(R,2) - pow(((2*c-pow(a,2))/(2*a)),2));
  }
  if(y1 >= y2){
    xc = x1;
    yc = y1;
  }
  else{
    xc = x2;
    yc = y2;
  }
  if(xp == 0){
    *angleBase = 90;
  }
  else{
    *angleBase = atan(zp/xp)*(180/PI) + 90;
  }
  /*les articulations sont aux coordonnées : (dans le plan)
  base = (0,0)
  epaule = (0,d0)
  coude = (xc,yc)
  poignet = (xp,yp+d3)
  main = (xp,yp)
  */
  //dapres le theoreme d'al-kashi
  //points : base epaule coude
  a = d0;
  b = d1;
  c = sqrt(pow(xc,2) + pow(yc,2));
  *angleEpaule = acos((pow(a,2) + pow(b,2) - pow(c,2))/(2*a*b))*(180/PI) - 90;
  if (xc < 0){
    *angleEpaule = 180 - *angleEpaule;
  }  
  //points : epaule coude poignet
  a = d1;
  b = d2;
  c = sqrt(pow(xp,2) + pow((yp+d3-d0),2));
  *angleCoude = acos((pow(a,2) + pow(b,2) - pow(c,2))/(2*a*b))*(180/PI);
  if ((((yp+d3)-d0)*xc) > xp*(yc-d0)){
    *angleCoude = 360 - *angleCoude;
  }
  a = d2;
  b = d3;
  c = sqrt(pow((xc-xp),2) + pow((yc-yp),2));
  *anglePoignet = acos((pow(a,2) + pow(b,2) - pow(c,2))/(2*a*b))*(180/PI);
  if (((yp-yc)*(xp-xc)) > (xp-xc)*(yp+d3-yc)){
    *anglePoignet = 360 - *anglePoignet;
  }
}

bool mouvement_base(double angleCible, double * angleBase){ //rapproche l'angle actuel de l'angle cible à chaque fois que la fonction est appelée, elle renvoie true une fois atteint
  bool retour = false;
  if(abs(angleCible - (*angleBase))<=0.2){
     bouger_servo(servoBase, angleCible);
     *angleBase = angleCible;
     retour = true;
  }
  else if(angleCible < (*angleBase)){
    bouger_servo(servoBase, (*angleBase) - 0.2);
    *angleBase = *angleBase - 0.2;
  }
  else{
    bouger_servo(servoBase, (*angleBase) + 0.2);
    *angleBase = *angleBase + 0.2;
  }
  return retour;
}

bool mouvement_epaule(double angleCible, double * angleEpaule){ //rapproche l'angle actuel de l'angle cible à chaque fois que la fonction est appelée, elle renvoie true une fois atteint
  bool retour = false;
  if(abs(angleCible - (*angleEpaule))<=0.2){
    bouger_servo(servoEpaule, angleCible);
    (*angleEpaule) = angleCible;
    retour = true;
  }
  else if(angleCible < (*angleEpaule)){
    bouger_servo(servoEpaule, (*angleEpaule) - 0.2);
    (*angleEpaule) = (*angleEpaule) - 0.2;
  }
  else{
    bouger_servo(servoEpaule, (*angleEpaule) + 0.2);
    (*angleEpaule) = (*angleEpaule) + 0.2;
  }
  return retour;
}

bool mouvement_coude(double angleCible, double * angleCoude){ //rapproche l'angle actuel de l'angle cible à chaque fois que la fonction est appelée, elle renvoie true une fois atteint
  bool retour = false;
  if(abs(angleCible - (*angleCoude))<=0.2){
    bouger_servo(servoCoude, angleCible);
    (*angleCoude) = angleCible;
    retour = true;
  }
  else if(angleCible < (*angleCoude)){
    bouger_servo(servoCoude, (*angleCoude) - 0.2);
    (*angleCoude) = (*angleCoude) - 0.2;
  }
  else{
    bouger_servo(servoCoude, (*angleCoude) + 0.2);
    (*angleCoude) = (*angleCoude) + 0.2;
  }
  return retour;
}

bool mouvement_poignet(double angleCible, double * anglePoignet){ //rapproche l'angle actuel de l'angle cible à chaque fois que la fonction est appelée, elle renvoie true une fois atteint
  bool retour = false;
  if(abs(angleCible - (*anglePoignet))<=0.5){
    bouger_servo(servoPoignet, angleCible);
    (*anglePoignet) = angleCible;
    retour = true;
  }
  else if(angleCible < (*anglePoignet)){
    bouger_servo(servoPoignet, (*anglePoignet) - 0.5);
    (*anglePoignet) = (*anglePoignet) - 0.5;
  }
  else{
    bouger_servo(servoPoignet, (*anglePoignet) + 0.5);
    (*anglePoignet) = (*anglePoignet) + 0.5;
  }
  return retour;
}

void bouger_bras
(double x, double y, double z, double *angleBase, double *angleEpaule, double *angleCoude, double *anglePoignet){
  double angleCibleBase;
  double angleCibleEpaule;
  double angleCibleCoude;
  double angleCiblePoignet;
  double angleBasePrec = angleCibleBase;
  bool mouvementFini = false;
  calcul_angles_bras(x, y, z, &angleCibleBase, &angleCibleEpaule, &angleCibleCoude, &angleCiblePoignet);
  if(angleBasePrec == angleCibleBase){ //si on a pas besoin de tourner, on ne retourne pas par l'état initial
    while(mouvementFini == false){
      mouvementFini = mouvement_epaule(90, angleEpaule);
      mouvementFini = mouvement_coude(40, angleCoude) && mouvementFini;
      mouvementFini = mouvement_poignet(60, anglePoignet) && mouvementFini;
      delay(7);
    }
    mouvementFini = false;
  }
  while(mouvement_base(angleCibleBase, angleBase) == false);
  while(mouvementFini == false){
    mouvementFini = mouvement_epaule(angleCibleEpaule, angleEpaule);
    mouvementFini = mouvement_coude(angleCibleCoude, angleCoude) && mouvementFini;
    mouvementFini = mouvement_poignet(angleCiblePoignet, anglePoignet) && mouvementFini;
    delay(7);
  }
  delay(200);
}
  

void bouger_servo(int servo, double angle){
  if(servo == servoBase){
    pca.writeMicroseconds(servo, map(angle + correctifBase, 0, 180, 550, 2730));
  }
  else if(servo == servoEpaule){
    pca.writeMicroseconds(servo, map(angle + correctifEpaule, 0, 180, 550, 2730));
  }
  else if(servo == servoCoude){
    pca.writeMicroseconds(servo, map(angle + correctifCoude, 180, 0, 550, 2730));
  }
  else if(servo == servoPoignet){
    pca.writeMicroseconds(servo, map(angle + correctifPoignet, 0, 180, 550, 2730));
  }
}
