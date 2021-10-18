<html lang="en">
<style>
    table {
        border-style: solid;
        border-width: 2px;
        border-color: black;
    }

    .reveal-if-active {
        opacity: 0;
        max-height: 0;
        overflow: hidden;
        transform: scale(0.8);
        transition: 0.5s;
    }

    input[type="radio"]:checked~.reveal-if-active,
    input[type="checkbox"]:checked~.reveal-if-active {
        opacity: 1;
        max-height: 100px;
        overflow: visible;
        transform: scale(1);
        /* margin-bottom: 50px; */
    }

    input[type="radio"]:checked~.marginadd50,
    input[type="checkbox"]:checked~.marginadd50 {
        margin-bottom: 50px;
    }

    input[type="radio"]:checked~.marginadd10,
    input[type="checkbox"]:checked~.marginadd10 {
        margin-bottom: 10px;
    }
</style>

<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <title>CSV decrypt 2</title>
</head>


<body>
    <div class="jumbotron text-center" style="background: #ccc;">
        <div class="container-fluid" style="margin-bottom: 20px;">
            <h1>CSV Decrypter</h1>
            <br>
            <h3>Input:</h3>
            <form enctype='multipart/form-data' action='' method='post'>

                <!-- process type -->
                <h5 style="margin: 10px;">Select processing type:</h5>
                <div>
                    <input type="radio" id="rad2" name="select" value="tscipherlib">
                    <label for="rad2">tscipherlib Decryption</label><br>
                    <!-- enc in -->
                    <div class="reveal-if-active marginadd10">
                        <h5 style="margin: 10px;">Encrypted string:</h5>
                        <label for="todecrypt">Enter encrypted string : <span style="color: red;">*</span> </label>
                        <input type='text' id="todecrypt" name='todecrypt' class="require-if-active" data-require-pair="#rad2">
                        <label for="kettodecrypt">Enter key : <span style="color: red;">*</span> </label>
                        <input type='text' id="kettodecrypt" name='kettodecrypt' class="require-if-active" data-require-pair="#rad2">
                        <br>
                    </div>
                </div>
                <div>
                    <input type="radio" id="rad4" name="select" value="Decryption">
                    <label for="rad4">Decryption using CSV</label><br>
                    <div class="reveal-if-active marginadd50">
                        <label for="todecrypt">Enter encrypted string : <span style="color: red;">*</span> </label>
                        <input type='text' id="todecrypt" name='todecrypt' class="require-if-active" data-require-pair="#rad4" style="margin-bottom: 10px; margin-top: 10px;">
                        <br>
                        <label>Upload OTPLC here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='lccsv' style="margin-bottom: 10px;" accept=".csv">
                        <br>
                        <label>Upload OTPUC here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='uccsv' style="margin-bottom: 10px;" accept=".csv">
                        <br>
                        <label>Upload OTPNum here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='numcsv' style="margin-bottom: 10px;" accept=".csv">
                    </div>
                </div>
                <div>
                    <br>
                    <h5>CSV Options</h5>
                    <input type="radio" id="rad1" name="select" value="CSV to table">
                    <label for="rad1">CSV to table</label><br>
                    <div class="reveal-if-active marginadd50">
                        <!-- lc -->
                        <h5 style="margin: 10px;">CSV Uploads:</h5>
                        <label>Upload OTPLC here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='lccsv' style="margin-bottom: 10px;" accept=".csv">
                        <br>
                        <!-- uc -->
                        <label>Upload OTPUC here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='uccsv' style="margin-bottom: 10px;" accept=".csv">
                        <br>
                        <!-- num -->
                        <label>Upload OTPNum here : <span style="color: red;">*</span> </label>
                        <input class="require-if-active" size='50' type='file' name='numcsv' style="margin-bottom: 10px;" accept=".csv">
                        <br>
                    </div>
                </div>
                <!-- <br>
                <br> -->
                <input type='submit' name='submit' value='Process' style="margin: 10px;">
            </form>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js" integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            <script>
                // https://css-tricks.com/exposing-form-fields-radio-button-css/
                var Formhider = {
                    init: function() {
                        this.applyConditionalRequired();
                        this.bindUIActions();
                    },
                    bindUIActions: function() {
                        $("input[type='radio'], input[type='checkbox']").on("change", this.applyConditionalRequired);
                    },
                    applyConditionalRequired: function() {
                        $(".require-if-active").each(function() {
                            var el = $(this);
                            if ($(el.data("require-pair")).is(":checked")) {
                                el.prop("required", true);
                            } else {
                                el.prop("required", false);
                            }
                        });
                    }
                };
                Formhider.init();
            </script>
<!-- havent closed the div or body so php can keep formatting 🤷‍♀️ -->
</html>

<?php
//echo ("<div class=\"container-fluid\">");
//echo ("<div class=\"jumbotron text-center\" style=\"background: #ccc;\">");
if (isset($_POST['submit'])) {
    if (!empty($_POST['select'])) {
        echo ("<h3>Output: </h3>");
        if ($_POST['select'] == "tscipherlib") {
            $chars = str_split($_POST['todecrypt']);
            // foreach ($chars as $char) {
            //     echo ($char);
            // }
            //echo ("<br>");
            if (!empty($_POST['kettodecrypt'])) {
                if (!empty($_POST['todecrypt'])) {
                    $k = ($_POST['kettodecrypt']);
                    $s = ($_POST['todecrypt']);
                    $x = decipherTs($s, $k);
                    echo ($x);
                }
            }
        } elseif ($_POST['select'] == "CSV to table") {
            readCsvAndOut("t");
        } elseif ($_POST['select'] == "Decryption") {
//            echo ("dec");
            csvToArray();
        } else {
            echo ("error (\$_POST['select'])");
        }
    } else {
        echo <<<WARN

        <div class="alert alert-warning" role="alert"> 
            Please select an option 
        </div>
        WARN;
    }
}
echo <<<DIVs

</div>
</div>
</body>
DIVs; // div and body for html closed here | should run on every run even if form not used | cba w/ any indent on it unless i consesnetnly do indent thruout php

// functs 
function readCsvAndOut($opt) {
    // 1 = ID, 0 = char
    // lc
    if ($opt == "t") {
        echo ("<br>");
        if (!file_exists($_FILES['lccsv']['tmp_name']) || !is_uploaded_file($_FILES['lccsv']['tmp_name'])) {
            echo <<<WARN

        <div class="alert alert-danger" role="alert">
            OTPLC has not been uploaded!
        </div>
      WARN;
        } else {
            if (strpos(($_FILES['lccsv']['name']), "OTPLC") !== false) { // check right file is ulpoaded
                echo ("<h5>Lowercase (OTPLC)</h5>");
                $handle = fopen($_FILES['lccsv']['tmp_name'], "r");
                echo <<<TABLESTART

            <table class="table">
                <thead class="thead-dark" >
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Character</th>
                    </tr>
                </thead>
                <tbody>
            TABLESTART;
                while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
//                    $data[0];
//                    $data[1];
                    if ($data[1] == "0") {
                        //$data[0] = "Ignore this ID"; // Id being 0 is an err w/ otp gen, might aswell skip it and hope we never have an id that is acc 0
                        continue;
                    }
                    echo <<<TABLECONTENT

                        <tr>
                            <th scope="row">$data[1]</th>
                            <td>$data[0]</td>
                        </tr>
                TABLECONTENT;
                }
                echo <<<TABLEEND

                </tbody>
            </table>

            TABLEEND;
                fclose($handle);
            } else {
                $fn = ($_FILES['lccsv']['name']);
                echo <<<WARN

            <div class="alert alert-warning" role="alert"> 
                The uploaded file $fn does not match the appropriate rules. Please check this is an OTPLC file. 
            </div>
            WARN;
            }
        }
        // uc
        if (!file_exists($_FILES['uccsv']['tmp_name']) || !is_uploaded_file($_FILES['uccsv']['tmp_name'])) {
            echo <<<WARN

        <div class="alert alert-danger" role="alert">
            OTPUC has not been uploaded!
        </div>
      WARN;
        } else {
            if (strpos(($_FILES['uccsv']['name']), "OTPUC") !== false) {
                echo ("<h5>Uppercase (OTPUC)</h5>");
                $handle = fopen($_FILES['uccsv']['tmp_name'], "r");
                echo <<<TABLESTART

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Character</th>
                    </tr>
                </thead>
                <tbody>
            TABLESTART;
                while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
//                    $data[0];
//                    $data[1];
                    if ($data[1] == "0") {
                        //$data[0] = "Ignore this ID";
                        continue;
                    }
                    echo <<<TABLECONTENT

                        <tr>
                            <th scope="row">$data[1]</th>
                            <td>$data[0]</td>
                        </tr>
                TABLECONTENT;
                }
                echo <<<TABLEEND

                </tbody>
            </table>

            TABLEEND;
                fclose($handle);
            } else {
                $fn = ($_FILES['uccsv']['name']);
                echo <<<WARN

            <div class="alert alert-warning" role="alert"> 
                The uploaded file $fn does not match the appropriate rules. Please check this is an OTPUC file. 
            </div>
            WARN;
            }
        }
        // num
        if (!file_exists($_FILES['numcsv']['tmp_name']) || !is_uploaded_file($_FILES['numcsv']['tmp_name'])) {
            echo <<<WARN

        <div class="alert alert-danger" role="alert">
            OTPNum has not been uploaded!
        </div>
      WARN;
        } else {
            if (strpos(($_FILES['numcsv']['name']), "OTPNum") !== false) {
                echo ("<h5>Numbers (OTPNum)</h5>");
                echo <<<TABLESTART

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Character</th>
                    </tr>
                </thead>
                <tbody>
            TABLESTART;
                $handle = fopen($_FILES['numcsv']['tmp_name'], "r");
                while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
//                    $data[0];
//                    $data[1];
                    if ($data[1] == "0") {
                        //$data[0] = "Ignore this ID";
                        continue;
                    }
                    echo <<<TABLECONTENT

                        <tr>
                            <th scope="row">$data[1]</th>
                            <td>$data[0]</td>
                        </tr>
                TABLECONTENT;
                }
                echo <<<TABLEEND

                </tbody>
            </table>

            TABLEEND;
                fclose($handle);
            } else {
                $fn = ($_FILES['numcsv']['name']);
                echo <<<WARN

            <div class="alert alert-warning" role="alert"> 
                The uploaded file $fn does not match the appropriate rules. Please check this is an OTPNum file. 
            </div>
            WARN;
            }
        }
    }
}

function csvToArray() {
    if (isset($_FILES['lccsv'])) {
        if (!file_exists($_FILES['lccsv']['tmp_name']) || !is_uploaded_file($_FILES['lccsv']['tmp_name'])) {
            echo <<<WARN

        <div class="alert alert-danger" role="alert">
            OTPLC has not been uploaded!
        </div>
      WARN;
            echo ($_FILES["uccsv"]["name"]);
      } else {
          if (strpos(($_FILES['lccsv']['name']), "OTPLC") !== false) { // check right file is ulpoaded
              echo ("<h5>Lowercase (OTPLC)</h5>");
              $handle = fopen($_FILES['lccsv']['tmp_name'], "r");
              while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                  if ($data[1] == "0") {
                      // Id being 0 is an err w/ otp gen, might aswell skip it and hope we never have an id that is acc 0
                      continue;
                  } else {
                      print_r($data);
                  }
              }
          } else {
              $fn = ($_FILES['lccsv']['name']);
              echo <<<WARN

            <div class="alert alert-warning" role="alert"> 
                The uploaded file $fn does not match the appropriate rules. Please check this is an OTPLC file. 
            </div>
            WARN;
                }
                fclose ($handle);
            }
    }
}



// tscipherlib conveted
function decipherTs($array, $key): string {
    $o = "";
    //echo ($array);
    $array = explode(",", $array);
    for ($i = 0; $i < count($array); $i++) {
        $j = ($i + 1);
        $m = (intval($array[$i]) - scrambleTs($j, $key));
        // $t = ($m % 255);
        // $a = (chr($m));
        //echo ($m . "<br>");
        echo (newmod($m, 255));
        echo (unichr(100));
        $o = ($o . unichr(newmod($m, 255)));
    }
    return $o;
}
// lot of echo for debug 😂
function scrambleTs($iterate, $key) {
    $interim = $iterate;
    $interim += (($key % 10) * $iterate);
    $interim += (floor($iterate) / 3);
    $interim += ($iterate * 2);
    $interim += (floor(9 * sin(deg2rad($iterate * 2))));
    //echo ($interim . "<br>");
    $interim = (floor($interim));
    // echo ($interim . "<br>");
    for ($i = 0; $i < 6; $i++) {
        $interimb = (sin(deg2rad($key * 2)) * (2**32));
        $interimb = (floor($interimb));
        $interimb = (($interimb * 3) ^ ($iterate * 7));
        //echo ($interimb . "<br>");
        $interimc = $interimb >> (5);
        $interimc = $interimc << (5);
        //echo ($interimc . "<br>");
        $interimd = $interimc << (3);
        $interime = (($interimb) ^ ($interimc));
        $interime += $interimd;
        //echo ($interime . "<br>");
        $interim -= $interime;
        //echo ($interim . "<br>");
    }
    $interim = (newmod($interim, 255));
    //echo $interim. "<br>";
    //echo ($interim + 255 . "<br>");
    return ($interim + 255);
}
// php mod is diff to python so need our own mod funct
function newmod($a, $b) {
    return ($a - $b * floor($a / $b));
}
// aslo need to have our own unicode chr funct as php cant do unicode 👌🙄
function unichr($x) {
    return mb_convert_encoding('&#' . intval($x) . ';', 'UTF-8', 'HTML-ENTITIES');
}

?>