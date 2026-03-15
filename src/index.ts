import { Hono } from 'hono'
import { cors } from 'hono/cors'

const app = new Hono()

app.use('*', cors())

app.get('/', (c) => {
  return c.json({
    status: 'success',
    message: 'Abdul Store - Pakistan Number Info API is running',
    usage: '/api?num=3359736848'
  })
})

app.get('/api', async (c) => {
  const num = c.req.query('num')

  if (!num) {
    return c.json({
      success: false,
      error: 'Please provide a number using ?num= parameter'
    }, 400)
  }

  try {
    const formData = new URLSearchParams()
    formData.append('post_id', '413')
    formData.append('form_id', '5e17544')
    formData.append('referer_title', 'Search SIM and CNIC Details - Instant Ownership Check')
    formData.append('queried_id', '413')
    formData.append('form_fields[search]', num)
    formData.append('action', 'elementor_pro_forms_send_form')
    formData.append('referrer', 'https://simownership.com/search/')

    const response = await fetch('https://simownership.com/wp-admin/admin-ajax.php', {
      method: 'POST',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://simownership.com',
        'Referer': 'https://simownership.com/search/',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    })

    if (!response.ok) {
      return c.json({
        success: false,
        error: 'Source service connection failed'
      }, 503)
    }

    const apiData: any = await response.json()

    if (apiData.success && apiData.data?.data?.results) {
      const results = apiData.data.data.results
      const formattedResults = results.map((res: any) => ({
        number: res.n || 'N/A',
        name: res.name || 'N/A',
        cnic: res.cnic || 'N/A',
        address: res.address || 'N/A'
      }))

      return c.json({
        success: true,
        count: formattedResults.length,
        results: formattedResults
      })
    } else {
      return c.json({
        success: false,
        error: 'No records found'
      }, 404)
    }
  } catch (error: any) {
    return c.json({
      success: false,
      error: error.message
    }, 500)
  }
})

// Legacy support
app.post('/search', async (c) => {
  const body = await c.req.json()
  const num = body.query || ''
  // Redirect internally or re-execute logic
  // For simplicity, we can just call the same logic
  // But Hono doesn't have internal redirection to routes as easily as Flask test_request_context
  // So we just handle it or return an error.
  return c.json({ error: 'Please use GET /api?num=...', success: false }, 400)
})

export default app
