const db = require('../config/database');

class UserController {
  async getWatchlist(req, res) {
    try {
      const result = await db.query(
        `SELECT w.*, s.name, s.exchange, s.sector
         FROM user_watchlist w
         JOIN stock_symbols s ON w.symbol = s.symbol
         WHERE w.user_id = $1
         ORDER BY w.created_at DESC`,
        [req.user.id]
      );

      res.json({ watchlist: result.rows });
    } catch (error) {
      console.error('Get watchlist error:', error);
      res.status(500).json({ error: 'Server error' });
    }
  }

  async addToWatchlist(req, res) {
    try {
      const { symbol, notes, alertPriceAbove, alertPriceBelow } = req.body;

      if (!symbol) {
        return res.status(400).json({ error: 'Symbol required' });
      }

      const result = await db.query(
        `INSERT INTO user_watchlist (user_id, symbol, notes, alert_price_above, alert_price_below)
         VALUES ($1, $2, $3, $4, $5)
         ON CONFLICT (user_id, symbol) DO UPDATE
         SET notes = $3, alert_price_above = $4, alert_price_below = $5
         RETURNING *`,
        [req.user.id, symbol.toUpperCase(), notes, alertPriceAbove, alertPriceBelow]
      );

      res.json({ watchlist: result.rows[0] });
    } catch (error) {
      console.error('Add to watchlist error:', error);
      res.status(500).json({ error: 'Server error' });
    }
  }

  async removeFromWatchlist(req, res) {
    try {
      const { symbol } = req.params;

      await db.query(
        'DELETE FROM user_watchlist WHERE user_id = $1 AND symbol = $2',
        [req.user.id, symbol.toUpperCase()]
      );

      res.json({ message: 'Removed from watchlist' });
    } catch (error) {
      console.error('Remove from watchlist error:', error);
      res.status(500).json({ error: 'Server error' });
    }
  }
}

module.exports = UserController;
