package domain

func Size(a int) string {
	switch {
	case a < 0:
		return "negative"
	case a < 10:
		return "small"
	case a < 100:
		return "large"
	case a < 1000:
		return "huge"
	}
	return "enormous"
}
