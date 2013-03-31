if "<?" in code:
	part, value = code.split("<?", 1)
	if "?>" not in part:
		code = '?>' + code