CREATE DATABASE `ciel2025` ;
USE `ciel2025`;

--
-- Structure de la table `etudiant`
--
CREATE TABLE `etudiant` (
  `idetudiant` int(11) NOT NULL,
  `nom` varchar(45) NOT NULL,
  `prenom` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `telephone` varchar(45) DEFAULT NULL
) ;

--
-- Index pour la table `etudiant`
--
ALTER TABLE `etudiant`
  ADD PRIMARY KEY (`idetudiant`);

--
-- AUTO_INCREMENT pour la table `etudiant`
--
ALTER TABLE `etudiant`
  MODIFY `idetudiant` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

--
-- Données de la table `etudiant`
--
INSERT INTO `etudiant` (`idetudiant`, `nom`, `prenom`, `email`, `telephone`) VALUES
(1, 'ADENET-LOUVET', 'Bryan', 'bryan.adenetl@gmail.com', '+596696051217'),
(2, 'BEAUSOLEIL', 'Patrice', 'patricebeausoleil96@gmail.com', '+596696720198'),
(3, 'CELESTINE', 'Jimmy', 'Jimmycelestine193@gmail.com ', '+596696615883'),
(5, 'EPHESTION', 'Jean-Eves', 'ephestionjeaneves11@gmail.com', '+596696003764'),
(6, 'GUILON', 'Gregory', 'gregoryguilon298@gmail.com', '+596696365364'),
(8, 'LOUIS-ALEXANDRE', 'Laetitia', 'laetitia.louisalexandre@gmail.com', '+596696090308'),
(9, 'MALCOUSU', 'Emmanuel', 'm.malcousu23@gmail.com', '+596696936600'),
(10, 'MARIE-SAINTE', 'Moise', 'moise.mariesainte@gmail.com', '+596696982649'),
(11, 'MICAA', 'Florian', 'micaa.florian7@gmail.com', '+596696737986'),
(12, 'MONTLOUIS', 'Alhan', 'tisire257@gmail.com', '+596696206114'),
(13, 'NEJA', 'Sebastien', 'nejsebastian5@gmail.com', '+596696521217'),
(14, 'PLATOF', 'Nathan', 'platof.nathan6@gmail.com', '+596696010816'),
(15, 'POMIES', 'Djayron', 'pomies.djayron26@gmail.com', '+596696503446'),
(16, 'ROGER', 'Bryan', 'Bryanrogerpro@gmail.com', '+596696061183'),
(17, 'TALLY', 'Noah', 'noah.tally972@gmail.com ', '+596696555714'),
(18, 'TARPAU', 'Francois-Xavier', 'Travailmatthieu971@gmail.com', '+596696265360'),
(19, 'TSENG-CHING', 'Enzo', 'enzotc8@gmail.com', '+596696160328'),
(20, 'VAUDRAN', 'Loann', 'vaudranloann@gmail.com', '');
