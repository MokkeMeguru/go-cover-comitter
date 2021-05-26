package domain_test

import (
	"github.com/stretchr/testify/require"
	"testing"

	"github.com/MokkeMeguru/go-cover-commenter/internal/domain"
)

func TestSize(t *testing.T) {
	t.Run("negative", func(t *testing.T) {
		require.Equal(t, "negative", domain.Size(-1))
	})
}
