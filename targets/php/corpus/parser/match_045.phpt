<?php
function test() {
    var_dump(match(x){});
    match(y){
        3, 4 => 5,
    };
}
try {
    test();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>