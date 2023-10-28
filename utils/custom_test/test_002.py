from pprint import pprint

list_ = [['89928.05', '3', '1.11/s'], ['92421.44', '1', '1.08/s'], ['94161.95', '2', '1.06/s'],
         ['91491.30', '2', '1.09/s'], ['1077627.75', '22', '0.09/s'], ['1024387.81', '61', '0.10/s'],
         ['382274.81', '71', '0.26/s'], ['943196.25', '70', '0.11/s'], ['90497.73', '3', '1.11/s'],
         ['91157.70', '2', '1.10/s'], ['93808.63', '2', '1.07/s'], ['90661.83', '2', '1.10/s'],
         ['1070659.62', '21', '0.09/s'], ['974660.19', '65', '0.10/s'], ['381786.28', '72', '0.26/s'],
         ['921660.56', '72', '0.11/s'], ['90661.83', '2', '1.10/s'], ['91491.30', '2', '1.09/s'],
         ['93984.96', '2', '1.06/s'], ['89605.73', '2', '1.12/s'], ['842941.69', '46', '0.12/s'],
         ['1003900.00', '63', '0.10/s'], ['382274.81', '71', '0.26/s'], ['947745.31', '69', '0.11/s'],
         ['90497.73', '2', '1.11/s'], ['91491.30', '2', '1.09/s'], ['94517.96', '1', '1.06/s'],
         ['91659.03', '1', '1.09/s'], ['851235.25', '47', '0.12/s'], ['1003900.00', '63', '0.10/s'],
         ['383249.03', '71', '0.26/s'], ['905054.06', '74', '0.11/s'], ['91157.70', '2', '1.10/s'],
         ['90497.73', '2', '1.11/s'], ['94339.62', '1', '1.06/s'], ['89126.56', '2', '1.12/s'],
         ['1077627.75', '22', '0.09/s'], ['1014040.44', '62', '0.10/s'], ['382274.81', '71', '0.26/s'],
         ['956771.44', '69', '0.10/s'], ['91575.09', '1', '1.09/s'], ['91659.03', '2', '1.09/s'],
         ['94786.73', '1', '1.05/s'], ['90579.71', '2', '1.10/s'], ['845341.69', '47', '0.12/s'],
         ['1003900.00', '63', '0.10/s'], ['383249.03', '71', '0.26/s'], ['877582.56', '78', '0.12/s'],
         ['90334.23', '2', '1.11/s'], ['90826.52', '2', '1.10/s'], ['94428.70', '2', '1.06/s'],
         ['90991.81', '2', '1.10/s'], ['837165.31', '48', '0.12/s'], ['1303766.25', '40', '0.08/s'],
         ['385215.41', '69', '0.26/s'], ['930194.44', '72', '0.11/s'], ['89928.05', '2', '1.11/s'],
         ['90252.70', '2', '1.11/s'], ['93283.58', '2', '1.07/s'], ['90826.52', '2', '1.10/s'],
         ['895159.31', '40', '0.11/s'], ['974660.19', '66', '0.10/s'], ['422599.16', '47', '0.24/s'],
         ['947745.31', '69', '0.11/s'], ['91911.76', '1', '1.09/s'], ['90909.09', '2', '1.10/s'],
         ['95147.48', '1', '1.05/s'], ['91074.68', '2', '1.10/s'], ['837165.31', '49', '0.12/s'],
         ['974660.19', '65', '0.10/s'], ['380821.28', '71', '0.26/s'], ['851364.38', '81', '0.12/s'],
         ['90497.73', '2', '1.11/s'], ['90991.81', '2', '1.10/s'], ['94966.77', '1', '1.05/s'],
         ['91491.30', '2', '1.09/s'], ['843050.00', '47', '0.12/s'], ['1303766.25', '41', '0.08/s'],
         ['380821.28', '72', '0.26/s'], ['938887.81', '70', '0.11/s'], ['91324.20', '5', '1.10/s'],
         ['89047.20', '6', '1.12/s'], ['91407.68', '6', '1.09/s'], ['88967.98', '4', '1.12/s'],
         ['848959.44', '64', '0.15/s'], ['1145120.00', '75', '0.12/s'], ['392661.72', '113', '0.41/s'],
         ['721548.50', '158', '0.24/s'], ['90415.91', '6', '1.11/s'], ['89766.61', '6', '1.11/s'],
         ['91659.03', '6', '1.09/s'], ['91743.12', '4', '1.09/s'], ['847979.75', '66', '0.15/s'],
         ['928701.31', '100', '0.15/s'], ['393247.50', '112', '0.40/s'], ['709572.62', '159', '0.24/s'],
         ['91324.20', '5', '1.10/s'], ['90826.52', '5', '1.10/s'], ['90661.83', '5', '1.10/s'],
         ['88888.89', '4', '1.12/s'], ['1036000.00', '38', '0.12/s'], ['917564.06', '105', '0.16/s'],
         ['421411.12', '85', '0.38/s'], ['720573.81', '159', '0.24/s'], ['90579.71', '6', '1.10/s'],
         ['90334.23', '5', '1.11/s'], ['92336.11', '6', '1.08/s'], ['89928.05', '5', '1.11/s'],
         ['854734.69', '64', '0.15/s'], ['925161.31', '103', '0.16/s'], ['391694.59', '114', '0.41/s'],
         ['718516.81', '159', '0.24/s'], ['88183.43', '6', '1.13/s'], ['89525.52', '5', '1.12/s'],
         ['90009.01', '6', '1.11/s'], ['89525.52', '4', '1.12/s'], ['842288.56', '66', '0.15/s'],
         ['953907.31', '100', '0.15/s'], ['422946.81', '84', '0.38/s'], ['720392.38', '157', '0.24/s'],
         ['91324.20', '5', '1.10/s'], ['89766.61', '5', '1.11/s'], ['93545.37', '4', '1.07/s'],
         ['91575.09', '4', '1.09/s'], ['853748.31', '64', '0.15/s'], ['941437.94', '102', '0.15/s'],
         ['391694.59', '114', '0.41/s'], ['709572.62', '162', '0.24/s'], ['88809.95', '7', '1.13/s'],
         ['88183.43', '5', '1.13/s'], ['89766.61', '5', '1.11/s'], ['88417.33', '5', '1.13/s'],
         ['855817.56', '64', '0.15/s'], ['938300.69', '102', '0.15/s'], ['391694.59', '113', '0.41/s'],
         ['725766.94', '158', '0.24/s'], ['90171.33', '5', '1.11/s'], ['89847.26', '5', '1.11/s'],
         ['91743.12', '5', '1.09/s'], ['91827.37', '4', '1.09/s'], ['1036000.00', '38', '0.12/s'],
         ['906918.25', '107', '0.16/s'], ['393633.66', '112', '0.40/s'], ['716558.38', '160', '0.24/s'],
         ['91575.09', '5', '1.09/s'], ['89766.61', '5', '1.11/s'], ['91575.09', '6', '1.09/s'],
         ['89605.73', '4', '1.12/s'], ['859595.88', '63', '0.15/s'], ['937908.50', '103', '0.15/s'],
         ['390732.19', '114', '0.41/s'], ['724605.94', '157', '0.24/s'], ['90252.70', '6', '1.11/s'],
         ['89847.26', '4', '1.11/s'], ['91743.12', '5', '1.09/s'], ['89928.05', '5', '1.11/s'],
         ['1031073.75', '38', '0.12/s'], ['1135193.88', '78', '0.13/s'], ['392078.84', '113', '0.41/s'],
         ['607964.69', '166', '0.17/s'], ['84602.37', '12', '1.18/s'], ['84530.86', '11', '1.18/s'],
         ['87719.30', '6', '1.14/s'], ['86655.11', '6', '1.15/s'], ['943714.81', '93', '0.26/s'],
         ['910790.94', '161', '0.18/s'], ['407989.44', '289', '0.76/s'], ['527497.88', '224', '0.23/s'],
         ['85470.09', '11', '1.17/s'], ['87489.06', '7', '1.14/s'], ['86206.90', '13', '1.16/s'],
         ['86956.52', '7', '1.15/s'], ['968290.88', '85', '0.25/s'], ['910344.88', '159', '0.17/s'],
         ['407166.22', '290', '0.76/s'], ['534676.62', '223', '0.23/s'], ['86132.64', '11', '1.16/s'],
         ['85836.91', '11', '1.16/s'], ['88573.96', '7', '1.13/s'], ['85324.23', '11', '1.17/s'],
         ['939984.12', '111', '0.25/s'], ['924942.56', '158', '0.17/s'], ['407214.47', '302', '0.77/s'],
         ['537456.94', '222', '0.23/s'], ['84674.01', '12', '1.18/s'], ['84745.77', '11', '1.18/s'],
         ['87336.24', '7', '1.14/s'], ['84602.37', '11', '1.18/s'], ['945414.00', '92', '0.26/s'],
         ['787836.25', '156', '0.17/s'], ['408144.88', '185', '0.77/s'], ['536314.69', '222', '0.23/s'],
         ['84317.03', '11', '1.19/s'], ['84317.03', '11', '1.19/s'], ['85324.23', '13', '1.17/s'],
         ['84602.37', '9', '1.18/s'], ['925080.44', '96', '0.26/s'], ['872978.69', '131', '0.14/s'],
         ['421180.16', '252', '0.70/s'], ['638665.25', '217', '0.23/s'], ['85251.49', '12', '1.17/s'],
         ['84889.65', '11', '1.18/s'], ['86281.27', '15', '1.16/s'], ['87183.96', '6', '1.15/s'],
         ['934713.25', '94', '0.26/s'], ['1095918.38', '131', '0.15/s'], ['421509.88', '257', '0.71/s'],
         ['601186.56', '197', '0.21/s'], ['86132.64', '11', '1.16/s'], ['86132.64', '10', '1.16/s'],
         ['89126.56', '7', '1.12/s'], ['87489.06', '6', '1.14/s'], ['926472.19', '112', '0.25/s'],
         ['894245.81', '164', '0.18/s'], ['408577.50', '286', '0.75/s'], ['516594.16', '228', '0.24/s'],
         ['85324.23', '12', '1.17/s'], ['86355.79', '10', '1.16/s'], ['86281.27', '10', '1.16/s'],
         ['87108.02', '6', '1.15/s'], ['934713.25', '95', '0.26/s'], ['917784.12', '160', '0.18/s'],
         ['407091.62', '187', '0.77/s'], ['534008.62', '222', '0.23/s'], ['87565.68', '7', '1.14/s'],
         ['86132.64', '10', '1.16/s'], ['88105.73', '6', '1.13/s'], ['87108.02', '6', '1.15/s'],
         ['953185.81', '92', '0.25/s'], ['867633.62', '125', '0.13/s'], ['421463.69', '263', '0.72/s'],
         ['526394.06', '225', '0.24/s'], ['85397.09', '11', '1.17/s'], ['88183.43', '7', '1.13/s'],
         ['85616.44', '12', '1.17/s'], ['85251.49', '10', '1.17/s'], ['943148.38', '92', '0.26/s'],
         ['910790.94', '161', '0.18/s'], ['409403.97', '287', '0.75/s'], ['595330.12', '198', '0.21/s'],
         ['92225.40', '3', '10.84/s'], ['92353.16', '3', '10.83/s'], ['96283.46', '2', '10.39/s'],
         ['92199.89', '1', '10.85/s'], ['1107629.50', '48', '0.90/s'], ['1460423.38', '42', '0.69/s'],
         ['428515.84', '57', '2.33/s'], ['985064.44', '91', '1.02/s'], ['91734.70', '2', '10.90/s'],
         ['92370.22', '3', '10.83/s'], ['96190.84', '2', '10.40/s'], ['91684.24', '2', '10.91/s'],
         ['1110085.38', '46', '0.90/s'], ['1464699.75', '40', '0.68/s'], ['428699.53', '57', '2.33/s'],
         ['984157.12', '83', '1.02/s'], ['91659.03', '2', '10.91/s'], ['91835.80', '3', '10.89/s'],
         ['94912.68', '1', '10.54/s'], ['91852.66', '1', '10.89/s'], ['1106405.50', '46', '0.90/s'],
         ['1464699.75', '40', '0.68/s'], ['427417.12', '57', '2.34/s'], ['981813.38', '92', '1.03/s'],
         ['90301.60', '3', '11.07/s'], ['90909.09', '2', '11.00/s'], ['94661.11', '2', '10.56/s'],
         ['90407.74', '1', '11.06/s'], ['1110085.38', '46', '0.90/s'], ['1464699.75', '40', '0.68/s'],
         ['427234.50', '55', '2.34/s'], ['972627.94', '93', '1.03/s'], ['92242.41', '3', '10.84/s'],
         ['92524.06', '2', '10.81/s'], ['96052.25', '2', '10.41/s'], ['92558.31', '1', '10.80/s'],
         ['1140429.38', '21', '0.88/s'], ['1464699.75', '40', '0.68/s'], ['428515.84', '57', '2.33/s'],
         ['976065.75', '94', '1.03/s'], ['91024.94', '4', '10.99/s'], ['91633.83', '1', '10.91/s'],
         ['95401.64', '2', '10.48/s'], ['91516.43', '1', '10.93/s'], ['1103965.88', '49', '0.91/s'],
         ['1456171.75', '41', '0.69/s'], ['427599.84', '58', '2.34/s'], ['983389.81', '90', '1.03/s'],
         ['91499.68', '4', '10.93/s'], ['92472.72', '2', '10.81/s'], ['96927.40', '2', '10.32/s'],
         ['92816.04', '2', '10.77/s'], ['1111157.62', '44', '0.90/s'], ['1464699.75', '41', '0.68/s'],
         ['428332.31', '57', '2.34/s'], ['976674.06', '90', '1.03/s'], ['91709.46', '3', '10.90/s'],
         ['92131.93', '1', '10.85/s'], ['95675.47', '1', '10.45/s'], ['92310.53', '1', '10.83/s'],
         ['1108856.00', '46', '0.90/s'], ['1458294.50', '42', '0.69/s'], ['428148.97', '58', '2.34/s'],
         ['975060.44', '85', '1.03/s'], ['92678.41', '3', '10.79/s'], ['92524.06', '1', '10.81/s'],
         ['97191.18', '1', '10.29/s'], ['92876.38', '1', '10.77/s'], ['1106405.50', '48', '0.90/s'],
         ['1460423.38', '41', '0.69/s'], ['427052.09', '57', '2.34/s'], ['955489.12', '92', '1.05/s'],
         ['90851.27', '2', '11.01/s'], ['92064.07', '1', '10.86/s'], ['95492.74', '2', '10.47/s'],
         ['91861.11', '1', '10.89/s'], ['1110085.38', '46', '0.90/s'], ['1469001.50', '38', '0.68/s'],
         ['427782.72', '57', '2.34/s'], ['965378.31', '87', '1.04/s'], ['90686.49', '5', '11.03/s'],
         ['90711.17', '5', '11.02/s'], ['93659.27', '3', '10.68/s'], ['89855.34', '3', '11.13/s'],
         ['1083654.75', '64', '0.92/s'], ['1441385.75', '91', '0.70/s'], ['425417.25', '93', '2.35/s'],
         ['941956.00', '141', '1.07/s'], ['90637.18', '5', '11.03/s'], ['90155.07', '3', '11.09/s'],
         ['93852.66', '3', '10.65/s'], ['90009.00', '7', '11.11/s'], ['1084828.88', '63', '0.92/s'],
         ['1441942.88', '90', '0.70/s'], ['425055.69', '94', '2.35/s'], ['949505.69', '143', '1.06/s'],
         ['90983.53', '5', '10.99/s'], ['91141.09', '3', '10.97/s'], ['94652.16', '3', '10.56/s'],
         ['91008.38', '7', '10.99/s'], ['1088366.25', '63', '0.92/s'], ['1441385.75', '91', '0.70/s'],
         ['425055.69', '93', '2.35/s'], ['942943.75', '137', '1.07/s'], ['91124.48', '5', '10.97/s'],
         ['90628.96', '4', '11.03/s'], ['94598.43', '3', '10.57/s'], ['91157.70', '2', '10.97/s'],
         ['1087184.62', '65', '0.92/s'], ['1441064.75', '92', '0.69/s'], ['425960.81', '93', '2.35/s'],
         ['938906.69', '136', '1.07/s'], ['90900.82', '2', '11.00/s'], ['90991.81', '3', '10.99/s'],
         ['93668.05', '7', '10.68/s'], ['90538.70', '3', '11.05/s'], ['1086005.38', '66', '0.92/s'],
         ['1438945.88', '89', '0.70/s'], ['425598.31', '93', '2.35/s'], ['940762.88', '143', '1.07/s'],
         ['89790.79', '5', '11.14/s'], ['91166.02', '3', '10.97/s'], ['93993.80', '6', '10.64/s'],
         ['90293.45', '3', '11.07/s'], ['1086005.38', '66', '0.92/s'], ['1441385.75', '91', '0.70/s'],
         ['425779.50', '93', '2.35/s'], ['952460.69', '149', '1.06/s'], ['91016.65', '5', '10.99/s'],
         ['90612.54', '5', '11.04/s'], ['94984.80', '3', '10.53/s'], ['90587.92', '3', '11.04/s'],
         ['1122530.25', '43', '0.89/s'], ['1441385.75', '91', '0.70/s'], ['425417.25', '94', '2.35/s'],
         ['952340.31', '139', '1.05/s'], ['90195.73', '5', '11.09/s'], ['91124.48', '5', '10.97/s'],
         ['95584.02', '3', '10.46/s'], ['91802.08', '3', '10.89/s'], ['1090737.50', '63', '0.92/s'],
         ['1437279.12', '91', '0.70/s'], ['425598.31', '93', '2.35/s'], ['954677.75', '149', '1.05/s'],
         ['90546.91', '5', '11.04/s'], ['90350.56', '5', '11.07/s'], ['94357.43', '3', '10.60/s'],
         ['90983.53', '3', '10.99/s'], ['1084828.88', '64', '0.92/s'], ['1442889.88', '91', '0.70/s'],
         ['425960.81', '93', '2.35/s'], ['957273.75', '139', '1.05/s'], ['90760.58', '5', '11.02/s'],
         ['90383.23', '4', '11.06/s'], ['93755.86', '3', '10.67/s'], ['90694.72', '3', '11.03/s'],
         ['1086005.38', '64', '0.92/s'], ['1437279.12', '91', '0.70/s'], ['426142.34', '93', '2.35/s'],
         ['957830.62', '136', '1.05/s'], ['86903.62', '11', '11.51/s'], ['87343.87', '6', '11.45/s'],
         ['88245.68', '6', '11.33/s'], ['86430.43', '6', '11.57/s'], ['1066604.38', '109', '0.95/s'],
         ['1387598.00', '205', '0.77/s'], ['424446.16', '258', '2.59/s'], ['898582.44', '250', '1.30/s'],
         ['86813.09', '11', '11.52/s'], ['87427.88', '6', '11.44/s'], ['88573.96', '6', '11.29/s'],
         ['86497.71', '6', '11.56/s'], ['1056356.50', '113', '0.95/s'], ['1391318.38', '204', '0.80/s'],
         ['424137.62', '253', '2.59/s'], ['894676.56', '255', '1.28/s'], ['87221.98', '11', '11.47/s'],
         ['87374.40', '6', '11.44/s'], ['88566.11', '6', '11.29/s'], ['86941.41', '11', '11.50/s'],
         ['1058283.38', '93', '0.95/s'], ['1359517.00', '167', '0.77/s'], ['424101.84', '257', '2.59/s'],
         ['892050.62', '255', '1.28/s'], ['86340.88', '11', '11.58/s'], ['86408.02', '6', '11.57/s'],
         ['88644.62', '6', '11.28/s'], ['86393.09', '6', '11.57/s'], ['1067619.62', '108', '0.95/s'],
         ['1387290.38', '202', '0.77/s'], ['424820.31', '267', '2.60/s'], ['891766.19', '256', '1.28/s'],
         ['86903.62', '11', '11.51/s'], ['87108.02', '6', '11.48/s'], ['89094.80', '10', '11.22/s'],
         ['86911.18', '7', '11.51/s'], ['1063647.00', '110', '0.95/s'], ['1395850.88', '204', '0.81/s'],
         ['424900.91', '262', '2.59/s'], ['902216.56', '253', '1.27/s'], ['87558.01', '11', '11.42/s'],
         ['87642.42', '8', '11.41/s'], ['88550.43', '6', '11.29/s'], ['87489.06', '6', '11.43/s'],
         ['1068609.50', '109', '0.94/s'], ['1391350.62', '205', '0.77/s'], ['424861.25', '257', '2.59/s'],
         ['905682.44', '249', '1.27/s'], ['86572.59', '8', '11.55/s'], ['87237.20', '7', '11.46/s'],
         ['88082.45', '6', '11.35/s'], ['86422.95', '6', '11.57/s'], ['1060881.25', '111', '0.94/s'],
         ['1400040.00', '201', '0.75/s'], ['424734.03', '252', '2.58/s'], ['907942.19', '249', '1.26/s'],
         ['86140.06', '11', '11.61/s'], ['86370.70', '6', '11.58/s'], ['87819.45', '8', '11.39/s'],
         ['86737.79', '6', '11.53/s'], ['1060945.12', '112', '0.95/s'], ['1403080.12', '185', '0.74/s'],
         ['424880.34', '267', '2.60/s'], ['898519.12', '259', '1.28/s'], ['85273.30', '11', '11.73/s'],
         ['85836.91', '6', '11.65/s'], ['86933.84', '6', '11.50/s'], ['85287.84', '6', '11.73/s'],
         ['1066372.00', '93', '0.94/s'], ['1399735.88', '208', '0.80/s'], ['424857.34', '262', '2.59/s'],
         ['894437.38', '253', '1.28/s'], ['85962.34', '7', '11.63/s'], ['86206.89', '7', '11.60/s'],
         ['87796.31', '6', '11.39/s'], ['86058.52', '11', '11.62/s'], ['1096699.75', '94', '0.94/s'],
         ['1384010.50', '203', '0.76/s'], ['425004.62', '262', '2.59/s'], ['889785.00', '254', '1.28/s'],
         ['90384.86', '4', '110.64/s'], ['90672.52', '4', '110.29/s'], ['93749.71', '12', '106.67/s'],
         ['90030.88', '16', '111.07/s'], ['1137286.50', '46', '8.79/s'], ['1483517.25', '40', '6.74/s'],
         ['428437.34', '63', '23.34/s'], ['970413.38', '95', '10.32/s'], ['92137.88', '3', '108.53/s'],
         ['92229.65', '3', '108.43/s'], ['96398.55', '13', '103.74/s'], ['92474.43', '16', '108.14/s'],
         ['1138451.62', '48', '8.78/s'], ['1484398.12', '38', '6.74/s'], ['428419.00', '63', '23.34/s'],
         ['987796.88', '95', '10.14/s'], ['91690.12', '4', '109.06/s'], ['91751.54', '4', '108.99/s'],
         ['96296.44', '13', '103.85/s'], ['92150.61', '16', '108.52/s'], ['1139229.62', '22', '8.78/s'],
         ['1480661.75', '40', '6.75/s'], ['427905.69', '63', '23.37/s'], ['985252.50', '95', '10.16/s'],
         ['91327.54', '4', '109.50/s'], ['91907.54', '4', '108.81/s'], ['96461.78', '13', '103.67/s'],
         ['91761.64', '16', '108.98/s'], ['1137286.50', '46', '8.79/s'], ['1483957.62', '38', '6.74/s'],
         ['428052.22', '63', '23.36/s'], ['984617.62', '95', '10.16/s'], ['91057.27', '4', '109.82/s'],
         ['91614.52', '4', '109.15/s'], ['95761.59', '13', '104.43/s'], ['91240.05', '16', '109.60/s'],
         ['1131496.50', '49', '8.84/s'], ['1484177.88', '39', '6.74/s'], ['427576.34', '64', '23.39/s'],
         ['983404.06', '96', '10.20/s'], ['92529.20', '4', '108.07/s'], ['92430.84', '4', '108.19/s'],
         ['96291.80', '13', '103.85/s'], ['92572.02', '16', '108.02/s'], ['1136123.62', '46', '8.80/s'],
         ['1483297.25', '40', '6.74/s'], ['427924.00', '63', '23.37/s'], ['985752.62', '95', '10.15/s'],
         ['91888.96', '4', '108.83/s'], ['92233.91', '2', '108.42/s'], ['96499.95', '13', '103.63/s'],
         ['92397.53', '16', '108.23/s'], ['1138710.75', '23', '8.78/s'], ['1483957.62', '38', '6.74/s'],
         ['427869.09', '63', '23.37/s'], ['986460.75', '95', '10.16/s'], ['92607.17', '4', '107.98/s'],
         ['92638.05', '1', '107.95/s'], ['96366.03', '13', '103.77/s'], ['92688.71', '16', '107.89/s'],
         ['1139083.50', '22', '8.78/s'], ['1482857.38', '40', '6.74/s'], ['428217.19', '63', '23.35/s'],
         ['987583.50', '95', '10.14/s'], ['91494.66', '4', '109.30/s'], ['91761.64', '4', '108.98/s'],
         ['95439.88', '13', '104.78/s'], ['91665.75', '17', '109.09/s'], ['1135865.62', '48', '8.81/s'],
         ['1480004.50', '38', '6.76/s'], ['428033.88', '64', '23.36/s'], ['981222.50', '95', '10.20/s'],
         ['90913.22', '4', '110.00/s'], ['91369.26', '4', '109.45/s'], ['94791.22', '13', '105.50/s'],
         ['90919.01', '17', '109.99/s'], ['1135736.75', '49', '8.81/s'], ['1482417.75', '38', '6.75/s'],
         ['428125.53', '64', '23.36/s'], ['979371.62', '97', '10.21/s'], ['91300.85', '7', '109.53/s'],
         ['91330.04', '6', '109.49/s'], ['94288.92', '15', '106.06/s'], ['91505.55', '19', '109.28/s'],
         ['1121347.38', '67', '8.92/s'], ['1474784.12', '92', '6.79/s'], ['425538.56', '115', '23.50/s'],
         ['952091.75', '153', '10.59/s'], ['90700.48', '7', '110.25/s'], ['90938.03', '6', '109.96/s'],
         ['93996.45', '15', '106.39/s'], ['90454.35', '19', '110.55/s'], ['1121866.62', '68', '8.91/s'],
         ['1458877.75', '94', '6.86/s'], ['426082.50', '116', '23.47/s'], ['948483.19', '173', '10.55/s'],
         ['91286.69', '6', '109.54/s'], ['91554.97', '6', '109.22/s'], ['94219.62', '15', '106.14/s'],
         ['90651.97', '19', '110.31/s'], ['1123236.38', '67', '8.90/s'], ['1477547.62', '92', '6.77/s'],
         ['426191.44', '116', '23.46/s'], ['950364.06', '146', '10.61/s'], ['91256.70', '6', '109.58/s'],
         ['91100.41', '6', '109.77/s'], ['94504.55', '15', '105.82/s'], ['90732.58', '19', '110.21/s'],
         ['1126652.88', '49', '8.88/s'], ['1458877.75', '94', '6.86/s'], ['426155.12', '115', '23.47/s'],
         ['950496.44', '141', '10.59/s'], ['90517.40', '7', '110.48/s'], ['90454.35', '6', '110.55/s'],
         ['93917.88', '15', '106.48/s'], ['89850.49', '19', '111.30/s'], ['1126399.12', '65', '8.88/s'],
         ['1470393.62', '93', '6.81/s'], ['426046.19', '116', '23.47/s'], ['948642.12', '152', '10.55/s'],
         ['91510.56', '6', '109.28/s'], ['91435.27', '6', '109.37/s'], ['94580.53', '15', '105.73/s'],
         ['91569.22', '19', '109.21/s'], ['1125021.50', '67', '8.89/s'], ['1475596.38', '91', '6.78/s'],
         ['425919.16', '116', '23.48/s'], ['956276.38', '142', '10.54/s'], ['91501.35', '6', '109.29/s'],
         ['91058.09', '6', '109.82/s'], ['94472.42', '15', '105.85/s'], ['91335.05', '19', '109.49/s'],
         ['1126795.88', '43', '8.88/s'], ['1469304.12', '91', '6.81/s'], ['426118.78', '115', '23.47/s'],
         ['950274.19', '182', '10.53/s'], ['90971.12', '6', '109.93/s'], ['90726.81', '6', '110.22/s'],
         ['94792.12', '16', '105.49/s'], ['90399.56', '19', '110.62/s'], ['1126145.38', '67', '8.88/s'],
         ['1458608.25', '95', '6.86/s'], ['426155.12', '115', '23.47/s'], ['951744.44', '181', '10.59/s'],
         ['90207.11', '6', '110.86/s'], ['90601.87', '6', '110.37/s'], ['94210.75', '15', '106.14/s'],
         ['90202.23', '19', '110.86/s'], ['1126652.88', '65', '8.88/s'], ['1465159.62', '93', '6.83/s'],
         ['426373.16', '116', '23.45/s'], ['948215.56', '189', '10.63/s'], ['90330.97', '6', '110.70/s'],
         ['90528.88', '6', '110.46/s'], ['93419.53', '15', '107.04/s'], ['89950.71', '19', '111.17/s'],
         ['1122228.12', '64', '8.91/s'], ['1476960.38', '90', '6.78/s'], ['426245.94', '116', '23.46/s'],
         ['944409.75', '156', '10.60/s'], ['85716.98', '14', '116.66/s'], ['85572.48', '9', '116.86/s'],
         ['87229.59', '19', '114.64/s'], ['85078.14', '18', '117.54/s'], ['1106139.88', '103', '9.05/s'],
         ['1477850.00', '163', '6.79/s'], ['424400.47', '256', '23.56/s'], ['939152.12', '255', '10.67/s'],
         ['86778.44', '15', '115.24/s'], ['86177.92', '10', '116.04/s'], ['88199.76', '20', '113.38/s'],
         ['85664.11', '24', '116.74/s'], ['1101873.50', '95', '9.09/s'], ['1471165.12', '203', '6.81/s'],
         ['424325.97', '278', '23.57/s'], ['937934.75', '256', '10.68/s'], ['86206.16', '14', '116.00/s'],
         ['86169.01', '10', '116.05/s'], ['87417.94', '20', '114.39/s'], ['85832.49', '19', '116.51/s'],
         ['1103209.25', '97', '9.07/s'], ['1463597.38', '210', '6.84/s'], ['424495.19', '265', '23.56/s'],
         ['935607.12', '262', '10.70/s'], ['85439.41', '15', '117.04/s'], ['85141.89', '11', '117.45/s'],
         ['86802.54', '21', '115.20/s'], ['84455.18', '19', '118.41/s'], ['1105912.88', '95', '9.05/s'],
         ['1464972.88', '206', '6.83/s'], ['424558.66', '271', '23.56/s'], ['936717.81', '256', '10.70/s'],
         ['85758.88', '14', '116.61/s'], ['85941.66', '11', '116.36/s'], ['87351.50', '21', '114.48/s'],
         ['85103.48', '20', '117.50/s'], ['1102147.00', '100', '9.08/s'], ['1471880.88', '205', '6.80/s'],
         ['424408.31', '270', '23.57/s'], ['936940.94', '255', '10.69/s'], ['87295.84', '15', '114.55/s'],
         ['86888.52', '11', '115.09/s'], ['88206.76', '21', '113.37/s'], ['86457.32', '20', '115.66/s'],
         ['1108183.38', '95', '9.03/s'], ['1469800.38', '209', '6.81/s'], ['424486.31', '273', '23.57/s'],
         ['935569.94', '256', '10.73/s'], ['86496.96', '11', '115.61/s'], ['86334.16', '11', '115.83/s'],
         ['87785.52', '21', '113.91/s'], ['85804.51', '20', '116.54/s'], ['1108344.62', '105', '9.03/s'],
         ['1473507.12', '164', '6.81/s'], ['424326.69', '257', '23.57/s'], ['936112.44', '256', '10.70/s'],
         ['84381.77', '14', '118.51/s'], ['83608.54', '12', '119.61/s'], ['85510.28', '21', '116.94/s'],
         ['84008.20', '21', '119.04/s'], ['1108291.25', '95', '9.02/s'], ['1470004.38', '208', '6.80/s'],
         ['423881.50', '255', '23.59/s'], ['937091.38', '255', '10.70/s'], ['85983.04', '15', '116.30/s'],
         ['86260.44', '12', '115.93/s'], ['87946.88', '22', '113.71/s'], ['85433.57', '21', '117.05/s'],
         ['1105612.38', '93', '9.05/s'], ['1468487.38', '164', '6.83/s'], ['423452.31', '264', '23.62/s'],
         ['936339.44', '256', '10.70/s'], ['85742.70', '15', '116.63/s'], ['85140.44', '12', '117.45/s'],
         ['86360.26', '22', '115.79/s'], ['84467.30', '22', '118.39/s'], ['1104184.88', '96', '9.06/s'],
         ['1473074.25', '163', '6.81/s'], ['424034.09', '256', '23.59/s'], ['937444.06', '281', '10.69/s']]


def dict_chunk(dicts, size):
    new_list = []
    dict_len = len(dicts)
    # 获取分组数
    while_count = dict_len // size + 1 if dict_len % size != 0 else dict_len / size
    split_start = 0
    split_end = size
    while while_count > 0:
        # 把字典的键放到列表中，然后根据偏移量拆分字典
        new_list.append([k for k in dicts[split_start:split_end]])
        split_start += size
        split_end += size
        while_count -= 1
    return new_list


res = dict_chunk(list_, 4)
list_1 = []
list_2 = []
for k, v in enumerate(res):
    if k % 2 == 1:
        list_1.append(v)
    else:
        list_2.append(v)

pprint(list_1)
# pprint(f'list_2:{list_2}')
