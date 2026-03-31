<?php

interface A {}
interface B {}

function test(): (A&B)|object {}

?>
===DONE===