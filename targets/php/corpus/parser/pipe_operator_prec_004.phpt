<?php

null
    |> (fn() => print (new Exception)->getTraceAsString() . "\n\n")
    |> (fn() => print (new Exception)->getTraceAsString() . "\n\n");

?>