<?php
ini_set('open_basedir', __DIR__);

$pathSeparator = PHP_OS_FAMILY !== 'Windows' ? ':' : ';';
$originalDir = __DIR__;
$tmpDir = $originalDir . '/gh10469_tmp';
@mkdir($tmpDir, 0777, true);
chdir($tmpDir);
ini_set('open_basedir', ini_get('open_basedir') . $pathSeparator . '.' . DIRECTORY_SEPARATOR . '..');
ini_set('open_basedir', ini_get('open_basedir') . $pathSeparator . '.' . DIRECTORY_SEPARATOR . '..' . DIRECTORY_SEPARATOR);
ini_set('open_basedir', ini_get('open_basedir') . $pathSeparator . '.' . DIRECTORY_SEPARATOR . 'a' . DIRECTORY_SEPARATOR);
ini_set('open_basedir', ini_get('open_basedir') . $pathSeparator . '.' . DIRECTORY_SEPARATOR . 'a');

chdir($originalDir);
var_dump(ini_get('open_basedir'));
var_dump(get_open_basedir());
?>